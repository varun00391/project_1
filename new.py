pipeline {
  agent any
  stages {
    stage('Git Version') {
      steps {
        sh 'which git'
        sh 'git --version'
      }
    }
  }
}
