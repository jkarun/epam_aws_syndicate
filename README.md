# epam_aws_syndicate


token: `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`

user name: `jkarun`

git path: `https://jkarun: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@github.com/jkarun/epam_aws_syndicate.git `

## setup process:
1. Setup project & navigate to newly created project folder in cmd
   ```syndicate generate project --name task02```
2. Setup environment variable to newly created project inside git repo
   ```setx SDCT_CONF C:\Users\arun_prasath\workspace\aws_tutorial\epam_aws_syndicate\task02\.syndicate-config-dev```
3. Setup syndicate configs by getting it from sandbox credentials popup
    ```syndicate generate config --name "dev" `
    --region "eu-central-1" `
    --bundle_bucket_name "syndicate-education-platform-custom-sandbox-artifacts-sbox02/134cb1e3/task02" `
    --prefix "cmtr-134cb1e3-" `
    --extended_prefix True `
    --iam_permissions_boundary "arn:aws:iam::905418349556:policy/eo_role_boundary" `
    --access_key "ASIA5FTZDTP2E6Y3MTZY" `
    --secret_key "BfYUPf3aR4zO6wyY69TJEz0fmcb6fmbnWZrIQRjb" `
    --session_token "IQoJb3JpZ2luX2VjEPX//////////wEaCXVzLWVhc3QtMSJGMEQCIFMq/cIxSBGyhvcNAjRAlIFdWam2UiTJlGUKe0cJo0X5AiA6KJMX4pS0F0vNaLrwhV6BxOLzJZVZa35gb+VYqjmuASrmAgj+//////////8BEAAaDDkwNTQxODM0OTU1NiIMp0zx7RtW5bXZiEx/KroCf7Xc3ToEPEDsr8NC3BLniB0ekZ4bcqvSod/VFwTlsZI+IANezJg+GWBtChcOdTyahr5Lvz8R0vCLuq7Pk0j0lI9GOOZ5ITTH8rA9w07+WLSVFYu0lkWGxT2NAmTRwpctDMMVEHEaFOfIlYKkFRIHt3tgCxc2XoTSZfVhAHq0G8RfgDAyhh3ZrHWuvauPHjVkwDh294/4ebp43xVqGx/g2C0tjI/nm3C9faYuKAnwjYPsyXiLsu6nx+qja/Ph00B6sHSdgcgnd1Al6xHuISMUSY0xgb/er83l/IXoMrcrfJHfPHcdS5taux0uzBR6tLh5oe5QuSE9pzRQoto0nMOHhsIf7WY55dlTszTPxXZwFxybrIlCv95W2g2jR2F7wLrdN/Pzl6fWe7rufj9Wkji1vzjKmywF6pt86uYwt7y1tgY6ngEoPQCG+ueN92k5aZ95MQ+mlfOu/lftI0QTkV/v1hReN9QgdRZQ0M/eagK5tWHxxq6fD3V6SoZA6COrP4mMrXBcjl4L6kR4AEbJUSynn2qP3rEwkbVC5ykkID9bP5Nj9Ff/xkl+7OVPqUl4yjs3uM0cTYvfGpHYERH5yt/cS4E9vtzPw5tareNp+yJUfVG6IdEHbZhOHyY3QLVQXSubcw=="```
4. Generate lambda function
   `syndicate generate lambda --name hello_world --runtime python`
5. Generate api gateway 
   `syndicate generate meta api_gateway  --resource_name demo-api  --deploy_stage api --minimum_compression_size 0`


syndicate generate meta api_gateway  --resource_name task3_api --deploy_stage api

syndicate generate meta api_gateway_resource --api_name task3_api --path /hello --enable_cors false 

syndicate generate meta api_gateway_resource_method --api_name task3_api --path /hello --method GET --integration_type HTTP --lambda_name cmtr-134cb1e3-hello_world --authorization_type AWS_IAM --api_key_required false 