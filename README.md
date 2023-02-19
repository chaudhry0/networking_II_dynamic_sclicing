<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/chaudhry0/networking_II_dynamic_sclicing/">
    <img src="images/logos_and_icons/logo.png" alt="Logo" width="400" height="100">
  </a>

<h3 align="center">On Demand SDN Slices in ComNetsEmu</h3>

  <p align="center">
    powered by Unitn students
    <br />
    <a href="https://docs.google.com/presentation/d/16mhrYgM1bwTjN1HjwxlCGBQPV1TGdutkFfXK27SI580/edit#slide=id.g1dd0e9f175d_0_7"><strong>Explore the Presentation »</strong></a>
    <br />
    <br />
    <a href="https://www.youtube.com/watch?v=mKPfAVHFmTE">View video Demo</a>
    ·
    <a href="https://github.com/chaudhry0/networking_II_dynamic_sclicing/issues">Report Bug</a>
    ·
    <a href="https://github.com/chaudhry0/networking_II_dynamic_sclicing/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#how-to-run">how to run</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-layout">Project Layout</a></li>
    <li><a href="#about-us">About Us</a></li>
    <li><a href="#contacts">Contacts</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![GUI image][GUI]](https://github.com/chaudhry0/networking_II_dynamic_sclicing/blob/main/images/GUI.png)

On Demand SDN Slices in ComNetsEmu is a project aimed at implementing a network slicing approach that allows for dynamic activation and de-activation of network slices via command line interface (CLI) or graphical user interface (GUI) commands. The goal of this project is to provide a flexible and efficient way to manage network resources in a virtualized environment.

With the increasing demand for various types of network services, network slicing has emerged as a promising solution to address this challenge. Network slicing allows multiple virtual networks to co-exist on the same physical infrastructure, each with its own characteristics and requirements. The On Demand SDN Slices in ComNetsEmu project implements this concept using software-defined networking (SDN) technology.

The project uses a single SDN controller, such as RYU, to manage the network slices. The user can activate and de-activate different slices on demand, depending on their specific requirements. The slices can be described using templates, which allow for easy identification of flows, topology, and link capacity for each slice.

Overall, On Demand SDN Slices in ComNetsEmu provides a powerful and versatile solution for managing network resources in a virtualized environment. With its ability to activate and de-activate slices on demand, it offers increased flexibility and efficiency for users.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
* [![Python][Python-logo]][Python-url]
* [![Visual Studio Code][VSC-logo]][VSC-url]
* [![MININET][Mininet-logo]][Mininet-url]
* [![ComNetsEmu][ComNetsEmu-logo]][Comnetsemu-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Welcome to our repository! In order to get started and have a working local copy of "On demand network slicig" follow these simple example steps.

### Prerequisites

Our software is developded inside <a href="https://git.comnets.net/public-repo/comnetsemu">ComNetsEmu</a>, a tested and network emulator designed for the NFV/SDN teaching book "Computing in Communication Networks: From Theory to Practice". ComNetsEmu extends the famous Mininet emulator to support better emulation of versatile NFV/SDN network applications. It extends and puts forward the concepts and work in the Containernet project.

* More detailed information <a href="https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-labs">here</a> 
```bash
$ cd ~
$ git clone https://git.comnets.net/public-repo/comnetsemu.git
$ cd ./comnetsemu
$ vagrant up comnetsemu
# Take a coffee and wait about 15 minutes

# SSH into the VM when it's up and ready (The ComNetsEmu banner is printed on the screen)
$ vagrant ssh comnetsemu
```


### Installation

* Instead, to get our software, follow the instruction below:  
1. Clone the repo
   ```sh
   git clone https://github.com/chaudhry0/networking_II_dynamic_sclicing
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- HOW TO RUN -->
## How to run

First go to this dir ./networking_II_dynamic_slicing/.  to run the following command:
1. Enable ryu controller to isolate the network topology into slices and creates the GUI:
   ```sh
   $ ryu-manager ryu_slice.py --observe-links
   ```
2. Network creation in Mininet (in a new terminal):
   ```sh
   $ sudo python3 topology.py
   ```
3. See real-time switches log file
   ```sh
   $ sudo tail -f /var/log/openvswitch/ovs-vswitchd.log
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

The goal of our project is to propose an implementation of a network slicing approach on-demand, therefore the user can be able to activate and deactivate different slices. 


_For more detail, please refer to the [VIDEO](https://www.youtube.com/watch?v=mKPfAVHFmT)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT LAYOUT -->
## Project Layout
```

└── [networking_II_dynamic_slicing]
     ├── [Images]
     │    ├── scenario1
     │    ├── scenario2
     │    ├── scenario3
     │    └── scenario4
     ├── ryu_sclice.py      
     ├── topology.py
     └── README.md
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ABOUT US -->
## About us

We are a team of three students pursuing a degree in Computer Science, Communications, and Electronics Engineering at the University of Trento. Our passion for technology and innovation led us to embark on this exciting project as part of the Networking II course, taught by the renowned Prof. Fabrizio Granelli.

The main focus of our project is software-defined networking and network slicing. Our aim was to create a system that could make on-demand network slicing in ComNetsEmu using Mininet and Python. This project has been a great opportunity for us to delve deeper into the world of networking and gain hands-on experience in this field.

We are proud of what we have accomplished and are eager to share our project with the world. Our aim is to contribute to the advancement of technology and help shape the future of networking. We believe that our project will have a positive impact on the industry and we are excited to see where this journey takes us.

If you have any questions or want to know more about our project, feel free to reach out to us through the emails listed in the next Section. 
We would be more than happy to hear from you.

<!-- CONTACT -->
## Contacts

-   Haroon Chaudhry Mohammad - [@twitter_handle](https://twitter.com/twitter_handle) - h.chaudhrymohammd@studenti.unitn.it
-   Giulio Zamberlan - [@twitter_handle](https://twitter.com/twitter_handle) - giulio.zamberlan@studenti.unitn.it
-   Francesco Poinelli - [@twitter_handle](https://twitter.com/twitter_handle) - francesco.poinelli@studenti.unitn.it


Project Link: [On Demand Network Slicing](https://github.com/chaudhry0/networking_II_dynamic_sclicing)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [Computing in Communication Networks: From Theory to Practice](https://cn.ifn.et.tu-dresden.de/compcombook/)
* [ComNetsEmu](https://git.comnets.net/public-repo/comnetsemu)
* [Mininet](http://mininet.org/)
* [Python](https://www.python.org/doc/)
* [VS Code](https://code.visualstudio.com/)
* [GitHub](https://github.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

Thank you for visiting our page!

[GUI]: images/GUI.png
[Python-logo]: https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat
[Python-url]: https://www.python.org/doc/
[VSC-logo]: https://img.shields.io/badge/-Visual%20Studio%20Code-007ACC.svg?logo=visual-studio-code&style=flat
[VSC-url]: https://code.visualstudio.com/
[Mininet-logo]: images/logos_and_icons/mininet.png
[Mininet-url]: http://mininet.org/
[Comnetsemu-logo]: images/logos_and_icons/comnetsemu.png
[Comnetsemu-url]: https://www.granelli-lab.org/researches/relevant-projects/comnetsemu-sdn-nfv-emulator
