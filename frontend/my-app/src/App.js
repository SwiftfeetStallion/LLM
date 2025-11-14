import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [history, setHistory] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState("not_allowed");

  useEffect(() => {
    const container = document.getElementById('messages');
    container.scrollTop = container.scrollHeight;
  }, [history])

  useEffect(() => {
    if (status === "active") { return; }
    if (prompt.trim() === "") { 
      setStatus("not_allowed");
      return;
    }
    setStatus("send_btn");
  }, [prompt, status])


  const makeQuery = async (query, new_history) => {
    setStatus("active");
    setHistory(new_history.concat([{"role": "system", "content": "Подождите..."}]))
    await fetch("http://localhost:3001/send", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: query
      })
    })
    .then(response => response.json())
    .then(data => 
      setHistory(new_history.concat([{"role": "system", "content": data}]))
    )
    .catch(error => console.log(error));
    setStatus("not_allowed")
  }

  const onSend = async () => {
      const new_history = history.concat([{"role": "user", "content": prompt.replace(/\n+/g, "\n")}]);
      setHistory(new_history);
      setPrompt('');
      await makeQuery(prompt, new_history);
  }

  const onDelete = (index) => {
    if (status === "active") {
      alert("Дождитесь генерации ответа, прежде чем удалить его");
      return;
    }
    const new_history = [...history.slice(0, index), ...history.slice(index + 1)];
    setHistory(new_history);
  }

  const onEmpty = () => {}

  const onGen = async (query) => {
    if (status === "active") {
      alert("Дождитесь ответа на предыдущий вопрос");
      return;
    }
    await makeQuery(query, history);
  }

  return ( <> 
  <div className='main_blk'>
    <div className='messages' id='messages'>
      <div className='introduction'>
        <h1>Здесь можно задать любой вопрос по</h1>
        <h1 className='c'>C++</h1>
      </div>
      {history.map((message, index) => 
        <div key={index} className={message.role === "user" ? "question" : 'response'}> 
          <p> {message.content} </p>
          <div className='btns'>
            {message.role === "user" ? <button className='gen_btn' onClick={() => onGen(message.content)}> Заново</button> : <></>}
            <button className='del_btn' onClick={() => onDelete(index)}>Удалить</button>
          </div>
        </div>
      )}
      </div>
  </div>

  <div className='question_blk'>
    <div className='textarea_blk'>
      <textarea placeholder='Введите запрос...' value={prompt} onChange={(event) => {
        setPrompt(event.target.value);
        if (status === "active") { return; }
        if (prompt.trim() === "") {
          setStatus("not_allowed");
          return;
        }
        setStatus("send_btn");
      }}></textarea>
      <div className='btn_blk'>
        <button className={status} 
        onClick={prompt.trim() === "" ? onEmpty : onSend}></button>
      </div>
    </div>
  </div>
    </>
  );
}

export default App;
