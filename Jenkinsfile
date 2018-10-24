pipeline {
  agent { 
    label { 
      label ""
      customWorkspace "${JENKINS_HOME}/workspace/${BRANCH_NAME}/${BUILD_NUMBER}" 
    }
  }
  stages {
    stage('test') {
      agent any
      steps {
        sh '''set +e
export PATH=$PYENV_ROOT:$PATH
pipenv install --python 3.7 --dev
RACK_ENV=test pipenv run pytest --junitxml ${WORKSPACE}/log/pytest/results.xml --cov-report xml tests/
pipenv --rm
'''
      }
    }
  }
  environment {
    dev = 'develop'
    PYENV_ROOT = '/var/lib/jenkins/.pyenv'
  }
  post {
    always{

      recordIssues(reportEncoding: '', sourceCodeEncoding: '', 
                   tools: [[id: '', name: '', pattern: 'log/prospector/pylint.log', tool: [$class: 'PyLint']],
                           [id: '', name: '', pattern: 'log/prospector/mypy.log', tool: [$class: 'MyPy']],
                           [id: '', name: '', pattern: 'log/prospector/pydocstyle.log', tool: [$class: 'PyDocStyle']],
                           [id: '', name: '', pattern: 'log/prospector/flake8.log', tool: [$class: 'Flake8']]])
      junit(testResults: 'log/pytest/results.xml', allowEmptyResults: true)
      junit(testResults: 'log/bandit/results.xml', allowEmptyResults: true)
      cobertura(autoUpdateHealth: true, autoUpdateStability: true, zoomCoverageChart: true,
                sourceEncoding: 'ASCII', coberturaReportFile: "coverage.xml")
    }
  }
}
