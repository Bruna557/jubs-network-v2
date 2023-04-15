import { useState } from "react"
import { Outlet } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux"
import { Row, Col } from "react-bootstrap"

import Navigation from "../components/Navigation/Navigations"
import UserCard from "../components/UserCard/UserCard"
import { fetchUser } from "../services/mocks/userService"
import { fetchRecommendation } from "../services/mocks/followService"
import { User } from "../types"
import { getUser, setUser } from "../store/userSlice"

import "./BaseLayout.scss"

const BaseLayout = () => {
  const dispatch = useDispatch()
  const user = useSelector(getUser)
  const [recommendation, setRecommendation] = useState<User[]>([])

  fetchUser(user.username).then(result => {
    dispatch(setUser(result))
  })

  fetchRecommendation(user.username).then(result => {
    setRecommendation(result)
  })

  return (
    <>
      <Navigation {...user}/>
      <Row className="content" id="scrollableDiv">
        <Col className="left-panel" md="3">
          <UserCard {...user} follow={false}/>
          <p className="people-text">People you may know</p>
          {recommendation.map((r: User, i: number) =>
            <Col key={i}>
              <UserCard {...r } follow={true}/>
            </Col>)}
        </Col>
        <Col className="outlet" md="6">
          <Outlet/>
        </Col>
        <Col className="right-panel" md="3">
          <img className="ad" src="/assets/ad.png" alt="ad"/>
        </Col>
      </Row>
    </>
  )
}

export default BaseLayout
