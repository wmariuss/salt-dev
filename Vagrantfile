# saltd environment
require 'fileutils'

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

WORKDIR = File.join(File.dirname(__FILE__))

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "saltd"
  config.vm.network "private_network", ip: "192.168.89.7"
  config.vm.network :forwarded_port, guest: 2223, host: 2233

  if File.directory?(File.expand_path("#{WORKDIR}"))
    config.vm.synced_folder "#{WORKDIR}", "/opt/saltd",
      owner: "vagrant", group: "vagrant"
  end
  
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
    vb.customize ["modifyvm", :id, "--cpus", 4]
    # Disable ubuntu cloudimg console log
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end

  # Install dependencies
  config.vm.provision "shell", path: "setup.sh"
end
