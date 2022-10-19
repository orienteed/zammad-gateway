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

## 🛒 Supported Platforms

<div style="display: flex; flex-direction: row; gap: 30px; margin: 20px 0">
    <a href="https://business.adobe.com/products/magento/magento-commerce.html" target="_blank">
        <div style="display: flex; flex-direction: column; justify-content: space-between; align-items: center">
            <img src="./resources/MagentoLogo.svg" width="" height="60">
            <p>Magento</p>
        </div>
    </a>
    <div style="display: flex; flex-direction: column; justify-content: space-between; align-items: center">
        <img src="./resources/ComingSoon.png" width="" height="60">
        <p>Stay tuned!</p>
    </div>
</div>

</br>

## ✅ Requirements

The requirements are:

- <a href="https://zammad.org/" target="_blank">Zammad</a>

To use Zammad Gateway you need to have a Zammad instance up and running. You can install it using the <a href="https://docs.zammad.org/en/latest/install/docker-compose.html" target="_blank">Zammad installation guide</a>.

- <a href="https://docs.docker.com/get-started/overview/" target="_blank">Docker</a>
- <a href="https://docs.docker.com/compose/" target="_blank">Docker Compose</a>

Docker and docker-compose are also required. If you don't have them installed, you can follow the <a href="https://docs.docker.com/engine/install/" target="_blank">Docker installation guide</a> and the <a href="https://docs.docker.com/compose/install/" target="_blank">Docker Compose installation guide</a>.

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
5. Now your gateway is running, you can see an endpoints summary in <a href="http://localhost:8081/docs" target="_blank">http://localhost:8081/docs</a>

</br>

<div align="center">
<b>
🚀 You can test every request using our Postman collection, click <a href="./resources/GatewayPostmanCollection.json" target="_blank">here</a> to download it 🚀
</b>
</div>

</br>

## 🙌🏼 How to contribute

To contribute to this project, you can do it in the following ways:

- Reporting bugs.
- Suggesting enhancements.
- Opening pull requests.

If you want to know more, please <a href="https://www.b2bstore.io/contact" target="_blank">contact us</a>

<hr>

<div align="center">
    <h3>Developed by</h3>
    <a href="https://www.orienteed.com/" target="_blank"><img src="./resources/OrienteedLogo.svg" width="" height="90" align = "middle"></a>
</div>
