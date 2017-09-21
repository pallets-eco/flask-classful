#
# Cookbook:: flask-classful
# Recipe:: docs
#
# Copyright:: 2017, The Authors, All Rights Reserved.

# flask-classful-docs project setup

# we need this because the guest path could change in the future
# instead of ~/workspace, it's likely that we'll use /mnt/workspace
cwd_path = node['teracy']['flask-classful-docs']['project_guest_path']

execute 'docker-compose pull --ignore-pull-failures --parallel' do
    cwd cwd_path
    command 'docker-compose pull --ignore-pull-failures --parallel'
end


execute 'docker-compose up -d' do
    cwd cwd_path
    command 'docker-compose up -d'
end
