import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-postbox',
  templateUrl: './postbox.component.html',
  styleUrls: ['./postbox.component.scss']
})
export class PostboxComponent {

  public cardData: any = {};
  @Input() public post: any = {};

  ngOnInit() {
    console.log("Post data", this.post);
  }

  likePost(post: any) {
    let index = this.post.findIndex((item: any) => item.post_id === post.post_id);
    this.post[index].liked = true
    this.post = [...this.post];
  }
}
