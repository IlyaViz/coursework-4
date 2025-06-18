import { Link } from "react-router";

const ConditionalLink = ({ to, children, condition }) => {
  if (condition) {
    return <Link to={to}>{children}</Link>;
  } else {
    return children;
  }
};

export default ConditionalLink;
