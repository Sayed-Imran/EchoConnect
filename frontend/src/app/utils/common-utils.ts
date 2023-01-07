export class CommonUtils {

  public static getAuthToken(): string {
    return localStorage.getItem("bearer-token") || "";
  }

  public static setAuthToken(token: string): void {
    localStorage.setItem("bearer-token", token);
  }

}
