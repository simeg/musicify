[%bs.raw {|require('./landing.css')|}];

[@bs.module] external img1: string = "../img/01.jpg";
[@bs.module] external img2: string = "../img/02.jpg";
[@bs.module] external img3: string = "../img/03.jpg";

let component = ReasonReact.statelessComponent("Landing");

let make = _children => {
  ...component,
  render: _self =>
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
        <div className="container">
          <a className="navbar-brand" href="#"> (ReasonReact.string("Start Bootstrap")) </a>
          <button
            className="navbar-toggler"
            _type="button"
            ariaControls="navbarResponsive"
            ariaExpanded=false
            ariaLabel="Toggle navigation">
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarResponsive">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item"> <a className="nav-link" href="#"> (ReasonReact.string("Sign Up")) </a> </li>
              <li className="nav-item"> <a className="nav-link" href="#"> (ReasonReact.string("Log In")) </a> </li>
            </ul>
          </div>
        </div>
      </nav>
      <header className="masthead text-center text-white">
        <div className="masthead-content">
          <div className="container">
            <h1 className="masthead-heading mb-0"> (ReasonReact.string("Musicify")) </h1>
            <h2 className="masthead-subheading mb-0" />
            <a href="#" className="btn btn-primary btn-xl rounded-pill mt-5" id="btn-start">
              (ReasonReact.string(" Start"))
            </a>
          </div>
        </div>
        <div className="bg-circle-1 bg-circle" />
        <div className="bg-circle-2 bg-circle" />
        <div className="bg-circle-3 bg-circle" />
        <div className="bg-circle-4 bg-circle" />
      </header>
      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6 order-lg-2">
              <div className="p-5"> <img className="img-fluid rounded-circle" src=img1 alt="" /> </div>
            </div>
            <div className="col-lg-6 order-lg-1">
              <div className="p-5">
                <h2 className="display-4"> (ReasonReact.string("For those about to rock...")) </h2>
                <p>
                  (
                    ReasonReact.string(
                      "Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Quod aliquid, mollitia odio veniam sit iste esse
                        assumenda amet aperiam exercitationem, ea animi
                        blanditiis recusandae! Ratione voluptatum molestiae
                        adipisci, beatae obcaecati.",
                    )
                  )
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <div className="p-5"> <img className="img-fluid rounded-circle" src=img2 alt="" /> </div>
            </div>
            <div className="col-lg-6">
              <div className="p-5">
                <h2 className="display-4"> (ReasonReact.string("We salute you!")) </h2>
                <p>
                  (
                    ReasonReact.string(
                      "Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Quod aliquid, mollitia odio veniam sit iste esse
                        assumenda amet aperiam exercitationem, ea animi
                        blanditiis recusandae! Ratione voluptatum molestiae
                        adipisci, beatae obcaecati.",
                    )
                  )
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section>
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6 order-lg-2">
              <div className="p-5"> <img className="img-fluid rounded-circle" src=img3 alt="" /> </div>
            </div>
            <div className="col-lg-6 order-lg-1">
              <div className="p-5">
                <h2 className="display-4"> (ReasonReact.string("Let there be rock!")) </h2>
                <p>
                  (
                    ReasonReact.string(
                      "Lorem ipsum dolor sit amet, consectetur adipisicing
                        elit. Quod aliquid, mollitia odio veniam sit iste esse
                        assumenda amet aperiam exercitationem, ea animi
                        blanditiis recusandae! Ratione voluptatum molestiae
                        adipisci, beatae obcaecati.",
                    )
                  )
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <footer className="py-5 bg-black">
        <div className="container">
          <p className="m-0 text-center text-white small"> (ReasonReact.string("Copyright &copy; Musicify 2018")) </p>
        </div>
      </footer>
    </div>,
};
