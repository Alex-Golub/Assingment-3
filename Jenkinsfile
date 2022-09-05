pipeline {
    agent any

    parameters {
        string name: 'SCAN_INTERVAL', defaultValue: '5'
        string name: 'PREVIOUS_TAG', defaultValue: "aws-${currentBuild.previousBuild != null ? currentBuild.previousBuild.number : "0"}"
        string name: 'BUILD_TAG', defaultValue: "aws-${currentBuild.number}"
    }

    environment {
        CONFIG = credentials('config')
    }

    stages {
        stage('Init') {
            steps {
                cleanWs()
                sh "docker kill ${params.PREVIOUS_TAG} || true"
                sh "docker rm ${params.PREVIOUS_TAG} || true"
                sh "docker rmi -f ${params.PREVIOUS_TAG} || true"
            }
        }

        stage('Get SCM') {
            steps {
                git 'https://github.com/Alex-Golub/Assingment-3.git'
            }
        }

        stage('Build') {
            steps {
                sh "cat $CONFIG | tee config"
                sh "docker build -t ${params.BUILD_TAG} ."
            }
        }

        stage('Deploy') {
            steps {
                sh "docker run -itd --name ${params.BUILD_TAG} --env SCAN_INTERVAL=${params.SCAN_INTERVAL} ${params.BUILD_TAG}"
            }
        }

        stage('Logs') {
            steps {
                sleep(10)
                sh "docker logs ${params.BUILD_TAG}"
            }
        }
    }
}
