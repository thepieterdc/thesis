#!/bin/sh

set -euxo

cd /app
commit=$1

git fetch origin $commit
git checkout $commit
git checkout -b "$commit-instrument"

# Reduce the amount of parallel workers.
sed -i "s/:number_of_processors/1/g" /app/test/test_helper.rb

# Disable the crud tests since coverage cannot be determined for them.
find /app/test/controllers -name "*_test.rb" | xargs sed -i 's/test_crud_actions/#test_crud_actions/g'

# Append cobertura to the Gemfile.
echo "gem 'simplecov-cobertura'" >> /app/Gemfile

# Set the formatter.
sed -i "s/require_relative/require 'simplecov-cobertura'\nSimpleCov.formatter = SimpleCov::Formatter::CoberturaFormatter\nrequire_relative/" /app/test/test_helper.rb

# Set the workflow action.
sed -i "s+bundle exec rails test+sh runner.sh\n    - uses: actions/upload-artifact@master\n      with:\n        name: reports\n        path: /tmp/run\n+" /app/.github/workflows/ruby.yml

# Remove the other workflows.
rm -f /app/.github/workflows/javascript.yml
rm -f /app/.github/workflows/release-drafter.yml
rm -f /app/.github/workflows/puppeteer.yml
rm -f /app/.github/workflows/capybara.yml

# Add the runscript.
cp /runner.sh /app/runner.sh

# Commit everything.
git config --global user.email "pieterdeclercq@outlook.com"
git config --global user.name "Your Name"

git add --all
git commit -a -m "$commit instrumented"
git push analysis +"$commit-instrument"

# Remove the runscript.
rm -f /app/runner.sh