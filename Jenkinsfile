// Jenkinsfile - API 回归测试 CI/CD 流水线

pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.10'
        TEST_ENVIRONMENT = 'test'
        SLACK_WEBHOOK = credentials('slack-webhook-url')
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    triggers {
        // 定时触发（每日凌晨2点）
        cron('0 2 * * *')
        // GitLab webhook 触发
        gitlab(triggerOnPush: true, triggerOnMergeRequest: true)
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Lint') {
            agent {
                docker {
                    image "python:${PYTHON_VERSION}"
                    reuseNode true
                }
            }
            steps {
                sh '''
                    pip install flake8 black isort
                    flake8 api_test_suite/ --max-line-length=120
                    black --check api_test_suite/
                    isort --check-only api_test_suite/
                '''
            }
        }
        
        stage('API Change Detection') {
            agent {
                docker {
                    image "python:${PYTHON_VERSION}"
                    reuseNode true
                }
            }
            steps {
                sh '''
                    pip install pyyaml deepdiff
                    python .github/scripts/detect_api_change.py \
                        --old-spec=openapi_old.yaml \
                        --new-spec=openapi.yaml \
                        --output=change_report.json
                '''
                archiveArtifacts artifacts: 'change_report.json', fingerprint: true
            }
        }
        
        stage('Regression Test - Test Environment') {
            agent {
                docker {
                    image "python:${PYTHON_VERSION}"
                    reuseNode true
                }
            }
            environment {
                BASE_URL = 'http://106.227.91.110:31000/api'
            }
            steps {
                sh '''
                    pip install -r api_test_suite/requirements.txt
                    pytest api_test_suite/ -v -s --tb=short \
                        --environment=test \
                        --base-url=${BASE_URL} \
                        --junitxml=results-test.xml \
                        --html=report-test.html \
                        --alluredir=allure-results
                '''
            }
            post {
                always {
                    junit 'results-test.xml'
                    archiveArtifacts artifacts: 'report-test.html', fingerprint: true
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report-test.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
        
        stage('Regression Test - Staging') {
            when {
                branch 'main'
            }
            agent {
                docker {
                    image "python:${PYTHON_VERSION}"
                    reuseNode true
                }
            }
            environment {
                BASE_URL = 'http://staging-api.example.com/api'
            }
            steps {
                sh '''
                    pip install -r api_test_suite/requirements.txt
                    pytest api_test_suite/ -v -s --tb=short \
                        --environment=staging \
                        --base-url=${BASE_URL} \
                        --junitxml=results-staging.xml \
                        --html=report-staging.html
                '''
            }
            post {
                always {
                    junit 'results-staging.xml'
                    archiveArtifacts artifacts: 'report-staging.html', fingerprint: true
                }
            }
        }
        
        stage('Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
    
    post {
        failure {
            script {
                sh """
                    curl -X POST "${SLACK_WEBHOOK}" \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "text": "API 回归测试失败!",
                            "attachments": [{
                                "color": "danger",
                                "fields": [{
                                    "title": "项目",
                                    "value": "${env.JOB_NAME}",
                                    "short": true
                                }, {
                                    "title": "构建号",
                                    "value": "${env.BUILD_NUMBER}",
                                    "short": true
                                }]
                            }]
                        }'
                """
            }
        }
        
        success {
            script {
                sh """
                    curl -X POST "${SLACK_WEBHOOK}" \
                        -H 'Content-Type: application/json' \
                        -d '{
                            "text": "API 回归测试通过 ✓",
                            "attachments": [{
                                "color": "good",
                                "fields": [{
                                    "title": "项目",
                                    "value": "${env.JOB_NAME}",
                                    "short": true
                                }, {
                                    "title": "构建号",
                                    "value": "${env.BUILD_NUMBER}",
                                    "short": true
                                }]
                            }]
                        }'
                """
            }
        }
    }
}
