class ButtonOption extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      kelas: this.props.kelas,
      level: this.props.level,
      dari: this.props.dari,
      label: this.props.label,
      message: this.props.message
    };
    this.optionHandler = this.optionHandler.bind(this);
  }

  optionHandler() {
    this.props.parentCallback({
      kelas: this.props.kelas,
      level: this.props.level,
      label: this.props.label,
      dari: this.props.dari,
      message: this.props.message
    });
  }

  render() {
    return /*#__PURE__*/ React.createElement(
      "button",
      {
        class: "button-option",
        onClick: this.optionHandler
      },
      this.state.message
    );
  }
}

class ChatUser extends React.Component {
  render() {
    return /*#__PURE__*/ React.createElement(
      "div",
      {
        class: "user-chat"
      },
      /*#__PURE__*/ React.createElement(
        "div",
        {
          class: "chatbox",
          style: {
            marginLeft: "auto"
          }
        },
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "messagebox",
            style: {
              textAlign: "right"
            }
          },
          this.props.msg
        )
      ),
      /*#__PURE__*/ React.createElement(
        "div",
        {
          class: "avatar"
        },
        /*#__PURE__*/ React.createElement("img", {
          src: "/static/bot.png",
          class: "bot-small"
        })
      )
    );
  }
}

class ChatBot extends React.Component {
  render() {
    return /*#__PURE__*/ React.createElement(
      "div",
      {
        class: "bot-chat"
      },
      /*#__PURE__*/ React.createElement("img", {
        src: "/static/bot.png",
        class: "bot-small"
      }),
      /*#__PURE__*/ React.createElement(
        "div",
        {
          class: "chatbox"
        },
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "messagebox"
          },
          this.props.msg
        )
      ),
      /*#__PURE__*/ React.createElement("div", {
        class: "avatar"
      })
    );
  }
}

class Bot extends React.Component {
  constructor() {
    super();
    this.display = [];
    this.option = [];
    this.choosenOption = "";
    this.state = {
      showdata: this.display,
      value: "",
      output: "Maaf kami tidak mengenali apa yang anda maksud",
      option: []
    };
    this.appendData = this.appendData.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.scrollToBottom = this.scrollToBottom.bind(this);
    this.handleCallback = this.handleCallback.bind(this);
    fetch("http://10.10.2.66:5000/api/option", {
      method: "GET"
    })
      .then((res) => res.json())
      .then((opt) => {
        this.display.push(
          /*#__PURE__*/ React.createElement(ChatBot, {
            msg: "Apakah ada yang bisa saya bantu ?"
          })
        );

        if (opt.length > 1) {
          for (var i = 0; i < opt.length; i++) {
            this.option.push(
              /*#__PURE__*/ React.createElement(ButtonOption, {
                parentCallback: this.handleCallback,
                kelas: opt[i]["kelas"],
                level: opt[i]["level"],
                dari: opt[i]["dari"],
                label: opt[i]["label"],
                message: opt[i]["message"]
              })
            );
          }
        }

        this.display.push(
          /*#__PURE__*/ React.createElement(
            "div",
            {
              style: {
                marginTop: "7px",
                display: "inline-block",
                marginBottom: "20px",
                marginLeft: "40px"
              }
            },
            this.option
          )
        );
        this.setState({
          showdata: this.display
        });
        this.option = [];
      });
  }

  handleCallback(childData) {
    const url =
      "http://10.10.2.66:5000/api/option?kelas=" +
      childData.kelas +
      "&level=" +
      (childData.level + 1) +
      "&label=" +
      childData.label +
      "&dari=" +
      childData.dari;
    this.choosenOption = childData.message;
    console.log(url);
    fetch(url, {
      method: "GET"
    })
      .then((res) => res.json())
      .then((opt) => {
        if (opt.length > 1) {
          for (var i = 0; i < opt.length; i++) {
            this.option.push(
              /*#__PURE__*/ React.createElement(ButtonOption, {
                parentCallback: this.handleCallback,
                kelas: opt[i]["kelas"],
                level: opt[i]["level"],
                dari: opt[i]["dari"],
                label: opt[i]["label"],
                message: opt[i]["message"]
              })
            );
          }

          this.display.push(
            /*#__PURE__*/ React.createElement(ChatBot, {
              msg: this.choosenOption
            })
          );
          this.display.push(
            /*#__PURE__*/ React.createElement(
              "div",
              {
                style: {
                  marginTop: "7px",
                  display: "inline-block",
                  marginBottom: "20px",
                  marginLeft: "40px"
                }
              },
              this.option
            )
          );
        } else {
          console.log(opt);
          const newline = opt[0]["message"]
            .split("\n")
            .map((str) => /*#__PURE__*/ React.createElement("p", null, str));
          this.display.push(
            /*#__PURE__*/ React.createElement(ChatBot, {
              msg: newline
            })
          );
          fetch("http://10.10.2.66:5000/api/option", {
            method: "GET"
          })
            .then((res) => res.json())
            .then((opt) => {
              this.display.push(
                /*#__PURE__*/ React.createElement(ChatBot, {
                  msg: "Apakah ada pertanyaan lain ?"
                })
              );

              if (opt.length > 1) {
                for (var i = 0; i < opt.length; i++) {
                  this.option.push(
                    /*#__PURE__*/ React.createElement(ButtonOption, {
                      parentCallback: this.handleCallback,
                      kelas: opt[i]["kelas"],
                      level: opt[i]["level"],
                      dari: opt[i]["dari"],
                      label: opt[i]["label"],
                      message: opt[i]["message"]
                    })
                  );
                }
              }

              this.display.push(
                /*#__PURE__*/ React.createElement(
                  "div",
                  {
                    style: {
                      marginTop: "7px",
                      display: "inline-block",
                      marginBottom: "20px",
                      marginLeft: "40px"
                    }
                  },
                  this.option
                )
              );
              setTimeout(() => {
                this.setState({
                  showdata: this.display
                });
                this.option = [];
              }, 1500);
            });
        }

        this.setState({
          showdata: this.display
        });
        this.option = [];
      });
  }

  scrollToBottom() {
    this.messagesEnd.scrollIntoView({
      behavior: "smooth"
    });
  }

  appendData(e) {
    e.preventDefault();
    fetch("http://10.10.2.66:5000/api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Access-Control-Allow-Origin": "http://10.10.2.66:5000",
        "Access-Control-Allow-Credentials": "true"
      },
      body: JSON.stringify({
        msg: this.state.value
      })
    })
      .then((res) => res.json())
      .then((output) => {
        const newline = output["message"]
          .split("\n")
          .map((str) => /*#__PURE__*/ React.createElement("p", null, str));
        this.setState({
          output: newline
        });
        this.display.push(
          /*#__PURE__*/ React.createElement(ChatUser, {
            msg: this.state.value
          })
        );
        this.display.push(
          /*#__PURE__*/ React.createElement(ChatBot, {
            msg: this.state.output
          })
        );
        this.setState({
          showdata: this.display,
          value: ""
        });
      });
    console.log("submit");
  }

  handleChange(e) {
    let inputvalue = e.target.value;
    this.setState({
      value: inputvalue
    });
  }

  componentDidMount() {
    function invoke() {
      var menu = $(".menu-bot");
      menu.css("display", "block");
      var tl = new TimelineMax();
      tl.to(menu, 0.5, {
        opacity: 1
      });
      tl.to(
        menu,
        1,
        {
          y: 0,
          ease: Power2.easeOut
        },
        0
      );
      var layout = $(".box-layout");
      tl.to(
        layout,
        0.2,
        {
          opacity: 0
        },
        0
      );
      $("#inputbox").focus();
    }

    $(".box-layout").click(function () {
      invoke();
    });
    this.scrollToBottom();
  }

  componentDidUpdate() {
    this.scrollToBottom();
  }

  render() {
    return /*#__PURE__*/ React.createElement(
      "div",
      null,
      /*#__PURE__*/ React.createElement(
        "div",
        {
          class: "menu-bot"
        },
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "header-menu"
          },
          /*#__PURE__*/ React.createElement(
            "div",
            {
              style: {
                margin: "13px 20px"
              }
            },
            /*#__PURE__*/ React.createElement("img", {
              id: "image-big",
              src: "/static/bot.png"
            }),
            /*#__PURE__*/ React.createElement(
              "div",
              {
                id: "font-big"
              },
              "Lastri SDM",
              /*#__PURE__*/ React.createElement(
                "span",
                {
                  id: "online"
                },
                "Online"
              )
            )
          )
        ),
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "main-menu"
          },
          /*#__PURE__*/ React.createElement("div", null, this.state.showdata),
          /*#__PURE__*/ React.createElement("div", {
            style: {
              float: "left",
              clear: "both"
            },
            ref: (el) => {
              this.messagesEnd = el;
            }
          })
        ),
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "footer-menu"
          },
          /*#__PURE__*/ React.createElement(
            "form",
            {
              id: "input-form",
              onSubmit: this.appendData
            },
            /*#__PURE__*/ React.createElement(
              "div",
              {
                class: "input-box"
              },
              /*#__PURE__*/ React.createElement("input", {
                type: "text",
                value: this.state.value,
                onChange: this.handleChange,
                name: "",
                placeholder: "Ketik pertanyaan anda disini",
                style: {
                  border: "none",
                  width: "100%"
                },
                id: "inputbox"
              })
            ),
            /*#__PURE__*/ React.createElement(
              "div",
              {
                class: "button-box"
              },
              /*#__PURE__*/ React.createElement(
                "button",
                {
                  id: "buttonz"
                },
                "\xA0"
              )
            )
          )
        )
      ),
      /*#__PURE__*/ React.createElement(
        "div",
        {
          class: "box-layout"
        },
        /*#__PURE__*/ React.createElement(
          "div",
          {
            class: "wrapper"
          },
          /*#__PURE__*/ React.createElement(
            "div",
            {
              id: "header-bot"
            },
            "Mau tanya Lastri ?"
          )
        ),
        /*#__PURE__*/ React.createElement("div", {
          id: "button-bot"
        })
      ),
      /*#__PURE__*/ React.createElement("div", {
        class: "main-layout"
      })
    );
  }
}

ReactDOM.render(
  /*#__PURE__*/ React.createElement(Bot, null),
  document.getElementById("app")
);