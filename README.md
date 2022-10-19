<img src="./resources/B2BStoreLogo.svg" width="" height="90" align = "left">
<h1>Zammad Gateway</h1>

</br>
</br>

- [📢 What is Zammad Gateway?](#-what-is-zammad-gateway)
- [✅ Requirements](#-requirements)
- [⚙️ Installation](#%EF%B8%8F-installation)
- [🙌🏼 How to contribute](#-how-to-contribute)

</br>

## 📢 What is Zammad Gateway?

Zammad Gateway is an excellent tool for those who want to integrate Zammad with external systems but don't have the knowledge or time to develop a custom integration.

It is an intermediate API that encapsulates/handles the authentication and requests to the Zammad Helpdesk API (like a wrapper) and exposes some endpoints to interact with them. The Gateway is a straightforward and effective way to integrate Zammad with third-party systems.

This software can be installed on a server and configured to listen for incoming requests from external systems. It then forwards those requests to Zammad using the Zammad Helpdesk API.

</br>

## ✅ Requirements

The requirements are:

- [Zammad](https://zammad.org/)

To use Zammad Gateway you need to have a Zammad instance up and running. You can install it using the [Zammad installation guide](https://docs.zammad.org/en/latest/install/docker-compose.html).

- [Magento](https://business.adobe.com/products/magento/magento-commerce.html)

Also, you need to have a Magento instance up and running. You can install it using the [Magento installation guide](https://devdocs.magento.com/guides/v2.4/install-gde/composer.html).

- [Docker](https://docs.docker.com/get-started/overview/)
- [Docker Compose](https://docs.docker.com/compose/)

Docker and docker-compose are also required. If you don't have them installed, you can follow the [Docker installation guide](https://docs.docker.com/engine/install/) and the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

</br>

## ⚙️ Installation

To install Zammad Gateway you need to follow these steps:

1. Clone the repository with:

```
git clone https://github.com/orienteed/zammad-gateway
```

2. Copy the _.env.example_ file to _.env_.
3. Fill _.env_ file with the required data.
4. Run the following command to start the gateway:

```
docker-compose up -d --build
```

5. Now your gateway is running, you can see an endpoint summary in http://localhost:8081/docs

</br>

<div align="center">
<b>
🚀 You can test every request using our Postman collection, click <a href="./resources/GatewayPostmanCollection.json">here</a> to download it 🚀
</b>
</div>

</br>

## 🙌🏼 How to contribute

If you want to contribute to this project, you can do it in the following ways:

- Reporting bugs.
- Suggesting enhancements.
- Opening pull requests.

If you want to contribute, please [contact us](https://www.b2bstore.io/contact)

</br>

<hr>

</br>

<div align="center">
    <h3>Developed by</h3>
    <a href="https://www.orienteed.com/"><img src="./resources/OrienteedLogo.svg" width="" height="90" align = "middle"></a>
</div>