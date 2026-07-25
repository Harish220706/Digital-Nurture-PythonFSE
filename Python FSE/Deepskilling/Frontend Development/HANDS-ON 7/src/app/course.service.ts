import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

@Injectable({ providedIn: 'root' })
export class CourseService {
  private apiUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=5';

  constructor(private http: HttpClient) {}

  // Task 2, step 96: fetch courses via HttpClient, mapped from placeholder posts
  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}
