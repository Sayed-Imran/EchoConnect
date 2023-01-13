const domain = "http://echo.crazeops.tech";
const host_domain = window.location.host;

export class Config {
  public static get BASE_POINT_API(): string {
    return `${domain}`;
  }
  public static get BASE_POINT_AUTH(): string {
    return this.BASE_POINT_API + ":30000/authenticate"
  }
  public static get BASE_POINT_POST(): string {
    return this.BASE_POINT_API + ":31000/api"
  }
  public static API_ENDPOINTS: any = {
    "login": this.BASE_POINT_AUTH + "/login",
    "register": this.BASE_POINT_AUTH + "/register",
    "googleLogin": this.BASE_POINT_AUTH + "/google_login",
    // "fetchAllCards"
    "allCards": this.BASE_POINT_POST + "/get-posts",

  }
}
