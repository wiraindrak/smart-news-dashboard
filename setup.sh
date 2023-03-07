# mkdir -p
echo PORT $PORT
echo "\
[general]\n\
email = \"wiraindrak@gmail.com\"\n\
" > credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > config.toml