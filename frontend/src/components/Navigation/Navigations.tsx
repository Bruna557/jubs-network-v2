import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useDispatch } from "react-redux"
import { Navbar, Container, Nav, NavDropdown, Form, Button, Modal } from "react-bootstrap"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faSearch } from "@fortawesome/free-solid-svg-icons"

import { User } from "../../types"
import { setBio, setPicture } from "../../store/userSlice"
import { changeBio, changePicture, changePassword } from "../../services/mocks/userService"
import "./Navigation.scss"

const Navigation = (user: User) => {
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState("")
  const [modalValue, setModalValue] = useState("")
  const [searchValue, setSearchValue] = useState("")

  const handleCloseModal = () => {
    setShowModal(false)
    setModalValue("")
  }
  const handleShowModal = (type: string) => {
    setShowModal(true)
    setModalType(type)
  }

  const handleSubmit = () => {
    if (modalType === "bio") {
      changeBio(user.username, modalValue)
        .then((response) => {
          dispatch(setBio(response.bio))
        })
        .catch(() => {
          navigate("/login")
        })
    } else if (modalType === "picture") {
      changePicture(user.username, modalValue)
        .then((response) => {
          dispatch(setPicture(response.picture))
        })
        .catch(() => {
          navigate("/login")
        })
    } else if (modalType === "password") {
      changePassword(user.username, modalValue)
        .catch(() => {
          navigate("/login")
        })
    }
    setShowModal(false)
    setModalValue("")
  }

  return (
    <>
      <Navbar collapseOnSelect expand="md" fixed="top">
        <Container>
          <Navbar.Brand>
            <Link to="/">
              <img src="/assets/logo.png" alt="logo"></img>
            </Link>
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="mx-auto">
              <Form className="d-flex ptb5">
                <Form.Control
                  type="text"
                  placeholder="Search users"
                  onChange={(e) => setSearchValue(e.target.value)}
                  value={searchValue}/>
                <Link to={{ pathname: '/search', search: `q=${searchValue}` }} onClick={() => setSearchValue("")}>
                  <Button className="search-button">
                    <FontAwesomeIcon icon={faSearch} />
                  </Button>
                </Link>
              </Form>
            </Nav>
            <Nav>
              <NavDropdown title={<img src={user.picture} alt="profile"></img>} id="profile-picture" align="end">
                <NavDropdown.Item onClick={() => handleShowModal("bio")}>Change bio</NavDropdown.Item>
                <NavDropdown.Item onClick={() => handleShowModal("picture")}>Change picture</NavDropdown.Item>
                <NavDropdown.Item onClick={() => handleShowModal("password")}>Change password</NavDropdown.Item>
                <NavDropdown.Item onClick={() => navigate("/login")}>Logout</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Modal centered show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>New {modalType}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="modal-form">
            {modalType !== "bio" && <input value={modalValue} onChange={(e) => setModalValue(e.target.value)} />}
            {modalType === "bio" && <textarea value={modalValue} onChange={(e) => setModalValue(e.target.value)} />}
          </form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Save
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default Navigation
