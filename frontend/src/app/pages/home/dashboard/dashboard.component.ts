import { Component, SimpleChanges } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Subject, takeUntil } from 'rxjs';
import { DefaultResponse } from 'src/app/models/default-response';
import { EchoToasterService } from 'src/app/services/echo-toaster.service';
import { visualizeService } from 'src/app/services/visualize.service';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent {
  public enableSidebar: any = false;
  public destroy$: Subject<boolean> = new Subject<boolean>();
  addclass: any = false;
  public selectedFile: any;
  public uploadData: any = {
    fileSelectedToUpload: '',
    file_extension: '',
    isValid: false,
    fileNameBlock: '',
    csvUploadFile: '',
    file: null,
  };
  public postDet: any = {}
  getAllPosts: any = [{
    "caption": "Test1",
    "description": "Testing",
    "tags": [
      "test"
    ],
    "post_id": "e2jpqVvz7Jo5GsTfjV6Mxf",
    "user_id": "TU2tnjjBRFCdMn64KGayLC",
    "object_url": "https://storage.googleapis.com/echo-connect-objects/e2jpqVvz7Jo5GsTfjV6Mxf.png",
    "created_at": "2023-01-12T08:39:48.252000",
    "updated_at": "2023-01-12T08:39:48.252000",
    "likes": 1,
    "user_profile": "",
    "user_name": ""
  },
  {
    "caption": "Test2",
    "description": "Testing",
    "tags": [
      "test"
    ],
    "post_id": "e2jpqVvz7Jo5GsTfjV6Mxf",
    "user_id": "TU2tnjjBRFCdMn64KGayLC",
    "object_url": "https://storage.googleapis.com/echo-connect-objects/e2jpqVvz7Jo5GsTfjV6Mxf.png",
    "created_at": "2023-01-12T08:39:48.252000",
    "updated_at": "2023-01-12T08:39:48.252000",
    "likes": 1,
    "user_profile": "",
    "user_name": ""
  }
  ];


  constructor(private visualService: visualizeService, private echoToasterService: EchoToasterService, private modalService: NgbModal) { }
  public openDropdown: any = false
  ngOnInit() {
    this.loadPost();
  }

  loadPost() {
    try {
      this.visualService.allPost({}).pipe(takeUntil(this.destroy$)).subscribe((respData) => {
        if (respData?.length) {
          this.getAllPosts = respData;
        }
        else {
          this.echoToasterService.show(respData || new DefaultResponse("failed", "Login Failed!"));
        }
      })

    } catch (posterr) {
      console.error(posterr);
    }
  }

  openSidebar() {
    this.enableSidebar = !this.enableSidebar
  }

  open(content: any) {
    this.modalService.open(content);
  }

  toggleDOMELM(referenceId: string) {
    try {
      const domEle = document.getElementById(referenceId);
      if (domEle) {
        domEle.click();
      }
    } catch (error) {
      console.error(error);
    }
  }


  uploadBlockCsv(event: any) {
    try {
      this.uploadData['isValid'] = false;
      const size = event.target.files[0].size / 1024 / 1024;
      if (size > 10) {
        this.uploadData['isValid'] = false;
        this.echoToasterService.show(new DefaultResponse("failed", "Cannot upload files more than 10 MB."));
        return;
      }
      if (event.target['value']) {
        const fileList: FileList = event.target.files;
        const validExts = new Array('.png', '.jpg', '.jpeg', '.jfif', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF', '.JFIF');
        let fileExt = JSON.parse(JSON.stringify(event.target['value']));
        fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
        this.uploadData['file_extension'] = fileExt;
        if (fileList.length > 0) {
          const file: File = fileList[0];
          if (validExts.indexOf(fileExt) > -1) {
            this.selectedFile = event.target.files[0];
            this.uploadData['fileSelectedToUpload'] = event.target['value'].split('\\').pop();
            this.uploadData['fileNameBlock'] = this.uploadData['fileSelectedToUpload'];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            const current = this;
            current.uploadData['isValid'] = true;
            reader.onload = function () {
              current.uploadData['csvUploadFile'] = reader.result;
              if (['.png', '.jpg', '.jpeg', '.jfif', '.gif', '.PNG', '.JPG', '.JPEG', '.GIF', '.JFIF'].includes(current.uploadData['file_extension'])) {
                // current.getSheetNames();
                console.log("file", current.selectedFile)
              } else {
                current.uploadData['sheet_name'] = null;
              }
            };
            reader.onerror = function (error) {
              console.error('Error: ', error);
            };
            // this.uploadBtn = true;
          } else {
            this.uploadData['isValid'] = false;
            this.echoToasterService.show(new DefaultResponse("failed", "Cannot upload files more than 10 MB."));
          }
        } else {
          this.uploadData['isValid'] = false;
        }
      }
    } catch (error) {
      console.error(error);
    }
  }

  uploadFile() {
    try {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('post', JSON.stringify(this.postDet));
      this.visualService.uploadPost(formData).pipe(takeUntil(this.destroy$)).subscribe((respData) => {
        if (respData?.length) {
          this.echoToasterService.show(respData || new DefaultResponse("Success", "File uploaded successfully"));
        }
        else {
          this.echoToasterService.show(respData || new DefaultResponse("failed", "failed to upload File"));
        }
      })

    } catch (posterr) {
      console.error(posterr);
    }
  }

  closeModal() {

  }
}
