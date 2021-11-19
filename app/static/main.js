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
          class: "avatar-bot"
        },
        /*#__PURE__*/ React.createElement("img", {
          src: "https://botsdm.pusri.co.id/static/bot.png",
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
        src: "https://botsdm.pusri.co.id/static/bot.png",
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
        class: "avatar-bot"
      })
    );
  }
}

class DownloadBot extends React.Component {
  render() {
    return /*#__PURE__*/ React.createElement(
      "div",
      {
        class: "bot-chat"
      },
      /*#__PURE__*/ React.createElement("img", {
        src: "https://botsdm.pusri.co.id/static/bot.png",
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
          "Anda dapat mendownload ",
          /*#__PURE__*/ React.createElement(
            "a",
            {
              href: this.props.msg,
              download: true
            },
            "Berkas"
          )
        )
      ),
      /*#__PURE__*/ React.createElement("div", {
        class: "avatar-bot"
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
      output: "Mohon maaf, lastri belum bisa jawab",
      option: []
    };
    this.appendData = this.appendData.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.scrollToBottom = this.scrollToBottom.bind(this);
    this.handleCallback = this.handleCallback.bind(this);
    fetch("http://localhost:5000/api/option", {
      method: "GET"
    })
      .then((res) => res.json())
      .then((opt) => {
        this.display.push(
          /*#__PURE__*/ React.createElement(ChatBot, {
            msg: "Apa yang bisa lastri bantu?"
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
      "http://localhost:5000/api/option?kelas=" +
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
        } else if (opt[0]["message"].split(" ")[0] == "!masukan") {
          fetch("http://localhost:5000/api/masukan", {
            method: "GET"
          });
          this.display.push(
            /*#__PURE__*/ React.createElement(ChatBot, {
              msg: "Ketik masukan dan pertanyaan anda, kami akan mencatat tanggapan anda sebagai bahan evaluasi kami kedepannya."
            })
          );
        } else {
          if (opt[0]["message"].split(" ")[0] == "!download") {
            let link = opt[0]["message"].split(" ")[1];
            this.display.push(
              /*#__PURE__*/ React.createElement(DownloadBot, {
                msg: link
              })
            );
          } else {
            const newline = opt[0]["message"]
              .split("\n")
              .map((str) => /*#__PURE__*/ React.createElement("p", null, str));
            this.display.push(
              /*#__PURE__*/ React.createElement(ChatBot, {
                msg: newline
              })
            );
          }

          fetch("http://localhost:5000/api/option", {
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
              }, 2500);
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
    var letter_and_spaces = /^[a-zA-Z\s]*$/; //Validation to the user_name input field

    if (!letter_and_spaces.test(this.state.value)) {
      this.display.push(
        /*#__PURE__*/ React.createElement(ChatBot, {
          msg: "Maaf kami hanya menerima pertanyaan berupa teks. Anda dapat masukan pertanyaan atau menekan tombol opsi pertanyaan diatas."
        })
      );
      this.setState({
        showdata: this.display,
        value: ""
      });
    } else if (!this.state.value.replace(/\s/g, "").length) {
      this.display.push(
        /*#__PURE__*/ React.createElement(ChatBot, {
          msg: "Masukan pertanyaan atau anda dapat menekan tombol opsi pertanyaan diatas"
        })
      );
      this.setState({
        showdata: this.display,
        value: ""
      });
    } else {
      fetch("http://localhost:5000/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Access-Control-Allow-Origin": "https://botsdm.pusri.co.id",
          "Access-Control-Allow-Credentials": "true"
        },
        body: JSON.stringify({
          msg: this.state.value
        })
      })
        .then((res) => res.json())
        .then((output) => {
          if (output["message"].indexOf("!menu") !== -1) {
            output["message"] = output["message"].replace("!menu", " ");
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
            fetch("http://localhost:5000/api/option", {
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
                }, 2500);
              });
          } else if (output["message"].indexOf("!download") !== -1) {
            output["message"] = output["message"].replace("!download", "");
            output["message"] = output["message"].replace(" ", "");
            this.display.push(
              /*#__PURE__*/ React.createElement(ChatUser, {
                msg: this.state.value
              })
            );
            this.display.push(
              /*#__PURE__*/ React.createElement(DownloadBot, {
                msg: output["message"]
              })
            );
            this.setState({
              showdata: this.display,
              value: ""
            });
            fetch("http://localhost:5000/api/option", {
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
                }, 2500);
              });
          } else {
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
          }
        });
      console.log("submit");
    }
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

    function closed() {
      var menu = $(".menu-bot");
      menu.css("display", "none");
      var tl = new TimelineMax();
      tl.to(menu, 0.5, {
        opacity: 0
      });
      tl.to(
        menu,
        1,
        {
          y: 1000,
          ease: Power2.easeOut
        },
        0
      );
      var layout = $(".box-layout");
      tl.to(
        layout,
        0.2,
        {
          opacity: 1
        },
        0
      );
    }

    $(".box-layout").click(function () {
      invoke();
    });
    $("#close-bot").click(function () {
      closed();
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
                backgroundColor: "transparent",
                padding: "13px 20px"
              }
            },
            /*#__PURE__*/ React.createElement("img", {
              id: "image-big",
              src: "https://botsdm.pusri.co.id/static/bot.png"
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
            ),
            /*#__PURE__*/ React.createElement(
              "div",
              {
                class: "close-box"
              },
              /*#__PURE__*/ React.createElement(
                "a",
                {
                  href: "#",
                  id: "close-bot"
                },
                "×"
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
                autocomplete: "off",
                type: "text",
                value: this.state.value,
                onChange: this.handleChange,
                name: "",
                placeholder: "Ketik pertanyaan anda disini",
                style: {
                  border: "none",
                  width: "100%",
                  backgroundColor: "transparent"
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
