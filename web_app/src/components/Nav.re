[%bs.raw {|require('./mix.css')|}];

let component = ReasonReact.statelessComponent("Mix");

let make = _children => {
  ...component,
  render: _self =>
    <nav
      className="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
      <div className="container">
        <a className="navbar-brand" href="#">
          (ReasonReact.string("Start Bootstrap"))
        </a>
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
            <li className="nav-item">
              <a className="nav-link" href="#">
                (ReasonReact.string("Sign Up"))
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="#">
                (ReasonReact.string("Log In"))
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>,
};
