#!groovy

import groovy.json.JsonSlurperClassic

// SCM data is no longer provided in environment variables when
// calling "checkout scm", it is now the return value of the call
def scmData = null
def logDir = "logs"

// This is a workaround for a bug in Jenkins - JENKINS-40574
// On the first run of the pipeline default parameters will not be set

pipeline {

    parameters {
        string(name: 'BRANCH', defaultValue: 'develop', description: 'The branch to build')
    }

    options {
        timeout(time: 45, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '10'))
        skipDefaultCheckout true
    }

    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        FLASK_APP = "${WORKSPACE}/CloudBash/api/main.py"
        PYTHONPATH = "${WORKSPACE}/CloudBash:${WORKSPACE}/CloudBash/api"
    }

    stages {

        stage('Checkout CICD') {
            steps {
                echo "${STAGE_NAME} Stage Execution Starting"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/unit_test_for_app']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'CloudBash-CICD']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[
                        credentialsId: 'da701aad-9139-4a8c-b2b9-32f5872d9de3',
                        url: 'https://github.com/DevSecOps-Project/CloudBash-CICD.git'
                    ]]
                ])
                dir('logs') {
                    writeFile file: 'dummy.txt', text: ""
                }
            }
            post {
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

        stage('Checkout App') {
            steps {
                echo "${STAGE_NAME} Stage Execution Starting"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'CloudBash']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[
                        credentialsId: 'da701aad-9139-4a8c-b2b9-32f5872d9de3',
                        url: 'https://github.com/DevSecOps-Project/CloudBash.git'
                    ]]
                ])
                dir('logs') {
                    writeFile file: 'dummy.txt', text: ""
                }
            }
            post {
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

    //     stage('Lint') {
    //         steps {
    //             dir('app') {
    //                 sh 'npm run lint'
    //             }
    //         }
    //     }

        stage('Setup Environment') {
            steps {
                script {
                    sh """#!/bin/bash
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install flask flask_restful requests pytest
                        python -c "import sys; print(sys.path)"
                    """
                }
            }
            post {
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    sh """#!/bin/bash
                        source ${VENV_DIR}/bin/activate
                        nohup python3 ${FLASK_APP} > flask_app.log 2>&1 &
                    """
                    sleep 10
                    sh """#!/bin/bash
                        source ${VENV_DIR}/bin/activate
                        export PYTHONPATH=${PYTHONPATH}
                        pytest ${WORKSPACE}/CloudBash/tests/test_api.py
                    """
                }
            }
            post {
                always {
                    script {
                        sh 'pkill -f "python3 ${FLASK_APP}"'
                    }
                }
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'python3 CloudBash-CICD/build_docker.py ${WORKSPACE}/CloudBash/api'
                }
            }
            post {
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

        stage('Upload Image') {
            steps {
                script {
                    sh 'python3 CloudBash-CICD/upload_image.py'
                }
            }
            post {
                success {
                    echo "${STAGE_NAME} Stage Finished Successfully"
                }
                failure {
                    echo "${STAGE_NAME} Stage Failed"
                }
            }
        }

    //     stage('Deploy to EKS') {
    //         steps {
    //             script {
    //                 sh '''
    //                     aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME}
    //                     kubectl set image deployment/${DEPLOYMENT_NAME} ${DEPLOYMENT_NAME}=${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace=${NAMESPACE}
    //                 '''
    //             }
    //         }
    //     }
    // }

    // post {
    //     success {
    //         script {
    //             slackSend(
    //                 channel: "${SLACK_CHANNEL}",
    //                 color: "good",
    //                 message: "Build ${env.BUILD_NUMBER} was successful. Deployed to ${CLUSTER_NAME}/${NAMESPACE}"
    //             )
    //         }
    //     }
    //     failure {
    //         script {
    //             slackSend(
    //                 channel: "${SLACK_CHANNEL}",
    //                 color: "danger",
    //                 message: "Build ${env.BUILD_NUMBER} failed. Check Jenkins for details."
    //             )
    //         }
    //     }
    //     always {
    //         cleanWs()
    //     }
    }
}
