Vagrant.configure("2") do |config|

  config.vm.provider "docker" do |d|
    d.image           = "quintenk/jenkins"
    d.has_ssh         = false
    d.ports           = ["8080:8080"]
    d.volumes	      = ["/data/jenkins:/root/.jenkins"]
  end

end
