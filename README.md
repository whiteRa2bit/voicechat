<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#docs">Docs</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Client-server sockets voice chat


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.


### Installation

- **Local**
  1. Clone the repo
     ```sh
     git clone https://github.com/whiteRa2bit/voicechat
     ```
  2. Create venv
     ```
     python3 -m venv venv
     . venv/bin/activate
     ```
  3. Install requirements
     ```
     pip3 install -r requirements.txt
     ```

- **Docker**

    You can either build an image yourself or pull a ready one from [Dockerhub](https://hub.docker.com/repository/docker/whitera2bit/voicechat)

    - Build
        ```
        docker build -t whitera2bit/voicechat . -f dockerfiles/Dockerfile
        ```

    - Pull from Dockerhub
        ```
        docker pull whitera2bit/voicechat
        ```

<!-- USAGE EXAMPLES -->
## Usage
First run server
- If you used local setup:
    ```
    python server.py
    ```

- If you used docker:
    ```
    docker run --name voicechat -t whitera2bit/voicechat /bin/bash
    python server.py
    ```

Then you can connect to a running server using:
- If you used local setup:
    ```
    python client.py
    ```

- If you used docker:
    ```
    docker exec -it voicechat /bin/bash
    python client.py
    ```

You will be asked to enter IP address and port of the running server

## Docs

Task description at docs/task.pdf

## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Pavel Fakanov - pavel.fakanov@gmail.com

Project Link: [https://github.com/whiteRa2bit/voicechat](https://github.com/whiteRa2bit/voicechat)
