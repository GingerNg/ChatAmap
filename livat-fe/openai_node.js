// import { Configuration, OpenAIApi } from "openai";
// import * as parse from "@fortaine/fetch-event-source/parse";
const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
  apiKey: "sk-*****",
  basePath:"http://localhost:8083/v1"
});

const openai = new OpenAIApi(configuration);
async function stream_help(){
  // refer: https://github.com/openai/openai-node/issues/18
  try {
    const messages =[
      {"role": "system", "content": "You are a writer, you are writing a story.返回10个字以内"},
      {"role": "user", "content": "你好"},
    ]
    const res = await openai.createChatCompletion({
      model: "gpt-3.5-turbo-0301",
      "messages": messages,
      max_tokens: 100,
      temperature: 0,
      stream: true,
  }, { responseType: 'stream' });

    // const res = await openai.createCompletion({
    //     model: "text-davinci-002",
    //     prompt: "It was the best of times",
    //     max_tokens: 100,
    //     temperature: 0,
    //     stream: true,
    // }, { responseType: 'stream' });

    res.data.on('data', data => {
        const lines = data.toString().split('\n').filter(line => line.trim() !== '');
        for (const line of lines) {
            console.log(line)
            const message = line.replace(/^data: /, '');
            console.log(message.length)
            console.log(message.trim() === '[DONE]')
            if (message.trim() === '[DONE]') {
                return; // Stream finished
            }
            try {
                const parsed = JSON.parse(message);
                console.log(parsed.choices[0].delta.content);
            } catch(error) {
                console.error('Could not JSON parse stream message', message, error);
            }
        }
    });
  } catch (error) {
    if (error.response?.status) {
        console.error(error.response.status, error.message);
        error.response.data.on('data', data => {
            const message = data.toString();
            try {
                const parsed = JSON.parse(message);
                console.error('An error occurred during OpenAI request: ', parsed);
            } catch(error) {
                console.error('An error occurred during OpenAI request: ', message);
            }
        });
    } else {
        console.error('An error occurred during OpenAI request', error);
    }
  }
}
stream_help()