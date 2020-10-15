FROM node:14

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./
COPY yarn.lock ./

# Install Node dependencies
RUN yarn install
COPY . .

EXPOSE 80
CMD [ "yarn", "start" ]