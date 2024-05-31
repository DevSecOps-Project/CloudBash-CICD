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

    stages {

        stage('Checkout CICD') {
            steps {
                echo "${STAGE_NAME} Stage Execution Starting"
                checkout([
                    changelog: false,
                    poll: false,
                    scm: [
                        $class: 'GitSCM',
                        branches: [[name: '*/upload_img_to_aws_stage']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [
                            [$class: 'RelativeTargetDirectory', relativeTargetDir: 'CloudBash-CICD']
                        ],
                        submoduleCfg: [],
                        userRemoteConfigs: [[
                            credentialsId: 'da701aad-9139-4a8c-b2b9-32f5872d9de3',
                            url: 'https://github.com/DevSecOps-Project/CloudBash-CICD.git'
                        ]]
                    ]
                ])
                // This is a workaround for a bug in Jenkins - JENKINS-47801
                // Cannot stash an empty dir therefore we create an empty dummy file inside the log dir
                dir(logDir){
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
                    changelog: false,
                    poll: false,
                    scm: [
                        $class: 'GitSCM',
                        branches: [[name: "*/${params.BRANCH}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [
                            [$class: 'RelativeTargetDirectory', relativeTargetDir: 'CloudBash']
                        ],
                        submoduleCfg: [],
                        userRemoteConfigs: [[
                            credentialsId: 'da701aad-9139-4a8c-b2b9-32f5872d9de3',
                            url: 'https://github.com/DevSecOps-Project/CloudBash.git'
                        ]]
                    ]
                ])
                // This is a workaround for a bug in Jenkins - JENKINS-47801
                // Cannot stash an empty dir therefore we create an empty dummy file inside the log dir
                dir(logDir){
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

        stage('Build Docker Image') {
            steps {
                sh """#!/bin/bash --login
                    python3 CloudBash-CICD/build_docker.py ${WORKSPACE}/CloudBash/api
                """
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

        stage('Unit Tests') {
            steps {
                sh """#!/bin/bash --login
                    sh nohup python3 ${WORKSPACE}/CloudBash/api/main.py
                """
                sleep 10
                sh """#!/bin/bash --login
                    sh export PYTHONPATH="${WORKSPACE}/CloudBash"
                    sh pytest ${WORKSPACE}/CloudBash/tests/test_api.py
                """
            }
            post {
                always {
                    sh """#!/bin/bash --login
                        sh pkill -f "python3 ${WORKSPACE}/CloudBash/api/main.py"
                    """
                }
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
                sh """#!/bin/bash --login
                    python3 CloudBash-CICD/upload_image.py
                """
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
