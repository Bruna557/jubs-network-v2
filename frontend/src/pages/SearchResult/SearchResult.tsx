import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"
import { Col } from "react-bootstrap"

import { User } from "../../types"
import UserCard from "../../components/UserCard/UserCard"
import { search } from "../../services/mocks/userService"
import "./SearchResult.scss"

const SearchResult = () => {
  const [users, setUsers] = useState<User[]>([])
  const [searchText, setSearchText] = useState("")
  const [searchParams] = useSearchParams();

  useEffect(() => {
    setSearchText(searchParams.get("q") || "")
    search(searchParams.get("q") || "").then(result => {
      setUsers(result)
    })
  }, [searchParams.get("q")])

  return (
    <>
      <h4>Search result: {searchText}</h4>
      <div className="results">
        {users.map((r: User, i:number) =>
          <Col key={i}>
            <UserCard {...r } follow={true}/>
          </Col>)}
      </div>
    </>
  )
}

export default SearchResult
