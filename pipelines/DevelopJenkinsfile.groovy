#!groovy

import groovy.json.JsonSlurperClassic

def scmData = null
def logDir = "logs"

pipeline {

    parameters {
        string(name: 'BRANCH', defaultValue: 'develop', description: 'The branch to build')
    }

    options {
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '7', numToKeepStr: '10'))
        skipDefaultCheckout true
    }

    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        PYTHONPATH = "${WORKSPACE}/CloudBash-CICD"
    }

    stages {

        stage('Checkout CICD') {
            steps {
                echo "${STAGE_NAME} Stage Execution Starting"
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/${BRANCH}']],
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

        stage('Setup Environment') {
            steps {
                script {
                    sh """#!/bin/bash
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install flask flask_restful requests pylint pytest
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

        stage('Pylint') {
            steps {
                script {
                    sh """#!/bin/bash
                        source ${VENV_DIR}/bin/activate
                        pylint --disable=missing-docstring,W0201,W0718,C0103,C0209,R0903  ${WORKSPACE}/CloudBash-CICD
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
                        export PYTHONPATH=${PYTHONPATH}
                        pytest ${WORKSPACE}/CloudBash-CICD/tests
                    """
                }
            }
            post {
                always {
                    script {
                        sh """#!/bin/bash
                            deactivate || true
                        """
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
    }
    
    post {
        always {
            script {
                if (currentBuild.result == null) {
                    currentBuild.result = 'SUCCESS'
                }
                sh """#!/bin/bash
                    BUILD_STATUS=${currentBuild.result} python3 CloudBash-CICD/notify.py
                """
            }
        }
    }
}
