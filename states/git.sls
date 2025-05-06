ensure_git_directory:
  file.directory:
    - name: /root/repos
    - user: root
    - group: root
    - makedirs: True

git_config_user:
  cmd.run:
    - name: |
        git config user.name "Jared"
        git config user.email "jared.d.elliottid@gmail.com"
    - cwd: /root/repos/backups
    - require:
      - file: ensure_git_directory

git_pull:
  git.latest:
    - name: git@github.com:getoutofmyyard/backups.git
    - target: /root/repos/backups
    - user: root
    - identity: /root/.ssh/id_rsa
    - require:
      - cmd: git_config_user

git_add:
  cmd.run:
    - name: git add --all
    - cwd: /root/repos/backups
    - user: root
    - require:
      - git: git_pull

git_commit:
  cmd.run:
    - name: git commit -m "Automated backup job"
    - cwd: /root/repos/backups
    - user: root
    - unless: |
        test -z "$(git status --porcelain)"
    - require:
      - cmd: git_add

git_push:
  cmd.run:
    - name: git push origin main
    - cwd: /root/repos/backups
    - user: root
    - require:
      - cmd: git_commit
