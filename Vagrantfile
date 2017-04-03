# Defines our Vagrant environment
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

# ---- Dependencies

require 'yaml'

# ---- Global variables

VAGRANT_VERSION     = 2
VAGRANT_CONFIG_FILE = "Vagrantconfig"

# ---- Default params

defaults = Hash.new
defaults['vm_name']   = 'flask'
defaults['vm_cpus']   = 1
defaults['vm_memory'] = 512
defaults['web_port']  = 5000

# ---- Loading params from YAML file

yaml = Hash.new
if File.exist?(VAGRANT_CONFIG_FILE)
  yaml = YAML::load_file(VAGRANT_CONFIG_FILE)
end

# ---- Mapping YAML parameters to my parameters (setting default values eventually)

params = Hash.new
defaults.each do |key, default_value|
  params[key] = yaml.has_key?(key) ? yaml[key] : default_value
end

# ---- Fixed params

params['vm_box'] = 'ubuntu/xenial64'

# ---- HACK to get all the directory mounted every time you reload

SYNCED_FOLDERS_CONFFILE=File.join(File.dirname(__FILE__), ".vagrant/machines/#{params['vm_name']}/virtualbox/synced_folders")
if File.exist?(SYNCED_FOLDERS_CONFFILE)
  File.delete(SYNCED_FOLDERS_CONFFILE)
end

# ---- Bootstrap script

bootstrap_script = <<SCRIPT
apt-get update
apt-get upgrade -y

apt-get install -y python python-virtualenv

if ! [ -d "/home/ubuntu/venv" ]; then
  cd /home/ubuntu
  sudo -u ubuntu virtualenv venv  
fi
SCRIPT

# ---- Vagrant configuration

Vagrant.configure(VAGRANT_VERSION) do |config|

  config.vm.define params['vm_name'] do |node|
    node.vm.box      = params['vm_box']
    node.vm.hostname = params['vm_name']

    node.vm.box_check_update = false

    node.vm.provider "virtualbox" do |vb|
      vb.name   = params['vm_name']
      vb.cpus   = params['vm_cpus']
      vb.memory = params['vm_memory']
    end

    node.vm.network "forwarded_port", guest: 5000, host: params['web_port']

    node.vm.synced_folder ".", "/vagrant", disabled: true
    node.vm.synced_folder ".", "/home/ubuntu/project"

    node.vm.provision :shell, inline: bootstrap_script
  end

end
