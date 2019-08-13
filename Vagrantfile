# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    # Official Ubuntu 18.04 LTS (Bionic Weaver)
    config.vm.box = "ubuntu/bionic64"
    config.vm.provision "shell", path: "setup.sh"
    config.disksize.size = '20GB'

    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # NOTE: This will enable public access to the opened port
    config.vm.network "forwarded_port", guest: 8088, host: 8088
    
    # Manually set provider if not automatically detected
    # config.vm.provider "vmware_fusion"
    # config.vm.provider "virtualbox"

    # Set VM properties 
    config.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.name = "ub-dev"
        vb.cpus = 1
        vb.memory = 1024
        vb.linked_clone = true

        # Enable host as DNS proxy in NAT mode
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
end
