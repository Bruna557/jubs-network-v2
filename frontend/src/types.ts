export type Post = {
  username: string,
  posted_on: string,
  body: string,
  likes: number,
  picture: string
}

export type User = {
  username: string,
  bio: string,
  picture: string
  follow?: boolean
}
