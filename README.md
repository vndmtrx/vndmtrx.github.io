## Blog Vndmtrx

#### [vndmtrx.github.io](https://vndmtrx.github.io)

### Instalação

```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
gem install bundler jekyll
bundle config set --local path 'vendor/bundle'
bundle install
bundle exec jekyll serve --host 0.0.0.0 --livereload --baseurl ''
```