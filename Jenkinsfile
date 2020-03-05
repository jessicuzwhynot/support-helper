pipeline {
    agent {
      node {
        label 'crate-ci'
      }
    }
    environment {
        DOCKER_COMMON_CREDS = credentials('crate-artifactory-deployer')
        DOCKER_USER = "$DOCKER_COMMON_CREDS_USR"
        DOCKER_PASS = "$DOCKER_COMMON_CREDS_PSW"
    }
    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
        stage('Test') {
            steps {
                sh './build.sh test'
            }
        }
        stage('Staging Deployment') {
            when {
                branch 'master'
            }
            steps {
                sh '''
                      docker login -u "$DOCKER_USER" -p "$DOCKER_PASS" dockerhub.cisco.com
                      ./build.sh publish --push --var tag=latest
                '''
            }
        }
        stage('Release Deployment') {
            when {
                buildingTag()
            }
            environment {
                TAG_NAME = "$BRANCH_NAME"
            }
            steps {
                sh '''
                      docker login -u "$DOCKER_USER" -p "$DOCKER_PASS" dockerhub.cisco.com
                      ./build.sh publish --push --var tag="$TAG_NAME"
                '''
            }
        }
    }
}