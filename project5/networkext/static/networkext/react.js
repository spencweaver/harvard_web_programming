// Load the posts using react
class Messages extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        items: []
      };
    }
  
    componentDidMount() {
      fetch("/react_messages")
        .then(result => result.json())
        .then(
          (result) => {
            this.setState({
              isLoaded: true,
              items: result
            });
          },
          // Check for errors
          (error) => {
            this.setState({
              isLoaded: true,
              error
            });
          }
        )
    }
  
    render() {
      const { error, isLoaded, items } = this.state;
      if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
          <div>
            <h1>My Messages</h1>
            <ul>
              {items.map(item => (
                <li key={item.id}>
                  {item.sender}: {item.body} 
                </li>
              ))}
            </ul>
  
          </div>
        );
      }
    }
  }
  
  // Render Template
  ReactDOM.render(<Messages />, document.getElementById('messages'));
  
  
  // Load the posts using react
  class Posts extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        items: []
      };
    }
  
    componentDidMount() {
      fetch("/react_post")
        .then(result => result.json())
        .then(
          (result) => {
            this.setState({
              isLoaded: true,
              items: result
            });
          },
          // Check for errors
          (error) => {
            this.setState({
              isLoaded: true,
              error
            });
          }
        )
    }
  
    render() {
      const { error, isLoaded, items } = this.state;
      if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
          <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.author}: {item.body} 
            </li>
          ))}
        </ul>
        );
      }
    }
  }
  
  // Render Template
  ReactDOM.render(<Posts />, document.getElementById('network'));
  
  
  // Load users so that they can message each other
  class Sendmessage extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        items: []
      };
    }
  
    componentDidMount() {
      fetch("/react_message")
        .then(result => result.json())
        .then(
          (result) => {
            this.setState({
              isLoaded: true,
              items: result
            });
          },
          // Check for errors
          (error) => {
            this.setState({
              isLoaded: true,
              error
            });
          }
        )
    }
  
  
    sendMessage = () => {
      this.setState({
        message: '',
      });
      // Set up for Post
      const requestMethod = {
        credentials: 'include',
        method: 'POST',
        body: JSON.stringify({ body: this.state.message }),
        headers: {'Content-Type': 'application/json', },
      };
      fetch(`react_message_send/7`, requestMethod)
      const data = response.json();
      console.log(data);
    }
  
    updateMessage = (event) => {
      this.setState({
          message: event.target.value
      });
    } 
  
    render() {
      const { error, isLoaded, items } = this.state;
      if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
          <div>
            <ul>
              {items.map(user => (
                <li key={user.user_id}>
                  {user.user_name} 
                    <input value={this.state.message} onKeyPress={this.inputKeyPress} onChange={this.updateMessage}></input>
                    <input type="submit" value="send" onClick={this.sendMessage}></input>
                </li>
              ))}
            </ul>
          </div>
        );
      }
    }
  }
  
  // Render Template
  ReactDOM.render(<Sendmessage />, document.getElementById('send_message'));