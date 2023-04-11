import { Link } from "react-router-dom"
import { Navbar, Container, Nav, Form, Button } from "react-bootstrap"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faSearch } from "@fortawesome/free-solid-svg-icons"

import "./Navigation.scss"

const Navigation = () => {
  return (
    <>
      <Navbar collapseOnSelect expand="md" fixed="top">
        <Container>
          <Navbar.Brand>
            <Link to="/">
              <img src="/assets/logo.png" alt="logo-"></img>
            </Link>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mx-auto">
              <Form className="d-flex ptb5">
                <Form.Control
                  type="text"
                  placeholder="Search users" />
                <Button className="search-button" type="submit">
                  <FontAwesomeIcon icon={faSearch} />
                </Button>
              </Form>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  )
}

export default Navigation
