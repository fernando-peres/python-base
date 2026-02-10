find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
find . -name "*.pyc" -exec rm -rf "{}" \;
find . -name ".DS_Store" -exec rm -rf "{}" \;
find . -name "__pycache__" -exec rm -rf "{}" \;
