import { useState } from "react"
import { Outlet } from "react-router-dom"
import { Row, Col, Button } from "react-bootstrap"

import Navigation from "../components/Navigation/Navigations"
import UserCard from "../components/UserCard/UserCard"
import { fetchUser } from "../services/mocks/userService"
import { fetchRecommendation } from "../services/mocks/followService"
import { User } from "../types"

import "./BaseLayout.scss"

const BaseLayout = () => {
  const [user, setUser] = useState<User>({ username: "", bio:"", picture:"" })
  const [recommendation, setRecommendation] = useState<User[]>([])

  fetchUser("bruna").then(result => {
    setUser(result)
  })

  fetchRecommendation("bruna").then(result => {
    setRecommendation(result)
  })

  return (
    <>
      <Navigation />
      <Row className="content">
        <Col className="left-panel" md="3">
          <UserCard {...user} />
          <p className="people-text">People you may know</p>
          {recommendation.map((r: User) =>
            <Row>
                <Col md="8">
              <UserCard {...r} />
              </Col>
              <Col>
                <Button>Follow</Button>
              </Col>
            </Row>
          )}
        </Col>
        <Col className="outlet" md="6">
          <Outlet />
        </Col>
        <Col className="right-panel" md="3">
          <img src="/assets/ad.png" />
        </Col>
      </Row>
    </>
  )
}

export default BaseLayout
