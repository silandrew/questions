file_to_disk1 = './disk-0-1.vdi'
file_to_disk2 = './disk-0-2.vdi'

Vagrant.configure("2") do |config|
  # Global conf
  config.ssh.insert_key = false
  config.vm.box_check_update = false
  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
  end

  # Create the first VM called repo
  config.vm.define :repo do |repo|
    repo.vm.box = "generic/rhel9"
    repo.vm.hostname = "repo"
    repo.vm.network :private_network, ip: "192.168.99.9"
    repo.vm.network :private_network, ip: "192.168.99.19"
    repo.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = "1"
      vb.customize ['storageattach', :id, '--storagectl', 'IDE Controller', '--port', '1', '--device', '0', '--type', 'dvddrive', '--medium', 'rhel-baseos-9.0-x86_64-dvd.iso']
    end
    repo.vm.provision :ansible do |ansible|
      ansible.playbook = "playbooks/repo.yml"
      ansible.inventory_path = "inventory"
      ansible.config_file = "ansible.cfg"
      ansible.limit = "repo"
      ansible.compatibility_mode = "2.0"
    end
  end

  # Create the second VM called server1
  config.vm.define :server1 do |server1|
    server1.vm.box = "generic/rhel9"
    server1.vm.hostname = "server1"
    server1.vm.network :private_network, ip: "192.168.99.10"
    server1.vm.network :private_network, ip: "192.168.99.110"
    server1.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = "2"
    end
    server1.vm.provision :ansible do |ansible|
      ansible.playbook = "playbooks/server1.yml"
      ansible.inventory_path = "inventory"
      ansible.config_file = "ansible.cfg"
      ansible.limit = "server1"
      ansible.compatibility_mode = "2.0"
    end
  end

  # Create the third VM called server2
  config.vm.define :server2 do |server2|
    server2.vm.box = "generic/rhel9"
    server2.vm.hostname = "server2"
    server2.vm.network :private_network, ip: "192.168.99.11"
    server2.vm.network :private_network, ip: "192.168.99.111"
    server2.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = "2"
      unless File.exist?(file_to_disk1)
        vb.customize ['createhd', '--filename', file_to_disk1, '--variant', 'Fixed', '--size', 16 * 1024]
      end
      unless File.exist?(file_to_disk2)
        vb.customize ['createhd', '--filename', file_to_disk2, '--variant', 'Fixed', '--size', 16 * 1024]
      end
      vb.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', file_to_disk1]
      vb.customize ['storageattach', :id,  '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', file_to_disk2]
    end
    server2.vm.provision :ansible do |ansible|
      ansible.playbook = "playbooks/server2.yml"
      ansible.inventory_path = "inventory"
      ansible.config_file = "ansible.cfg"
      ansible.limit = "server2"
      ansible.compatibility_mode = "2.0"
    end
  end
end