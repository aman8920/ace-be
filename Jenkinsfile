pipeline {
  agent any

  environment {
    // ACR & Image settings
    ACR_NAME        = 'acematureacr'                                    // e.g. 'myregistry'
    IMAGE_REPO      = "${ACR_NAME}.azurecr.io/ace-be"            // adjust for frontend/backend
    IMAGE_TAG       = "${env.BUILD_NUMBER}"
    FULL_IMAGE      = "${IMAGE_REPO}:${IMAGE_TAG}"

    // Helm settings
    HELM_RELEASE    = 'ace-be-helmchart'
    HELM_CHART_PATH = './ace-be-helmchart'                             // or path to your parent chart
    HELM_NAMESPACE  = 'ace-project'

    // Credentials IDs in Jenkins
    ACR_CRED_ID     = 'acr-creds'
    AZURE_SP_ID     = 'azure-sp'
    KUBECONFIG_ID   = 'aks-kubeconfig'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        script {
          docker.withRegistry("https://${ACR_NAME}.azurecr.io", ACR_CRED_ID) {
            // build the Docker image
            def img = docker.build(FULL_IMAGE, "-f backend.Dockerfile .")
            // push to ACR
            img.push()
            // optional: push latest tag
            //img.push('latest')
          }
        }
      }
    }

    stage('Deploy to AKS via Helm') {
      steps {
        script {
          // Define a temporary kubeconfig path
          def kubeconfig = 'kubeconfig-temp.yaml'

          // Use SP and other Azure credentials securely
          withCredentials([
            usernamePassword(credentialsId: AZURE_SP_CRED_ID, usernameVariable: 'AZ_CLIENT_ID', passwordVariable: 'AZ_CLIENT_SECRET'),
            string(credentialsId: AZURE_TENANT_ID_ID, variable: 'AZ_TENANT_ID'),
            string(credentialsId: AZURE_SUB_ID_ID, variable: 'AZ_SUBSCRIPTION_ID')
          ]) {
            sh """
              az login --service-principal -u $AZ_CLIENT_ID -p $AZ_CLIENT_SECRET --tenant $AZ_TENANT_ID
              az account set --subscription $AZ_SUBSCRIPTION_ID
              az aks get-credentials --resource-group <RG_NAME> --name <AKS_NAME> --file ${kubeconfig} --overwrite-existing

              export KUBECONFIG=${kubeconfig}
              helm dependency update ${HELM_CHART_PATH}

              helm upgrade --install ${HELM_RELEASE} ${HELM_CHART_PATH} \
                --namespace ${HELM_NAMESPACE} \
                --create-namespace \
                --set image.repository=${IMAGE_REPO} \
                --set image.tag=${IMAGE_TAG}
            """
          }
        }
      }
    }
  }

  post {
    success {
      echo " Deployment succeeded: ${FULL_IMAGE}"
    }
    failure {
      echo " Deployment failed"
    }
  }
}
