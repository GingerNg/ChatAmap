const { translate } = require('@vitalets/google-translate-api');

const express = require('express');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// https://github.com/vitalets/google-translate-api

app.post('/translate', (req, resp) => {
  console.log(req.body); // 输出 POST 请求的内容
  if (req.body.lang == "en2zh") {
    dest_lang = "zh-CN";
  }else{
    dest_lang = "en";
  }
  translate(req.body.text, { to: dest_lang }).then(res => {
    console.log(res.text);
    resp.send({"text": res.text, "status": 1}); // 返回响应
  }).catch(err => {
    console.error(err);
    resp.send({"text": "", "status": 0}); // 返回响应
  });
});

app.listen(3001, () => {
  console.log('Server started on port 3001');
});