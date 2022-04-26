FROM node:17.9.0-alpine3.15
WORKDIR /Project/frontend/
RUN npm install -g create-react-app
RUN npm install react-router-dom --save
RUN npm install @chakra-ui/icons
#初回のみコマンドラインで下記を実施すること
# docker-compose run --rm frontend sh -c "npx create-react-app app --template @chakra-ui/typescript"