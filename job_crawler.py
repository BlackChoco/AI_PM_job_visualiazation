import requests
import time
import json
import os
import re

class Meituan_Jobcrawler:
    def __init__(self,name:str):
        self.name = name

        if not os.path.exists(f'{self.name}'):
            os.makedirs(f'{self.name}')
    
    def crawl_fuc(self, url:str,headers:dict,payload:dict,crawl_type=str) -> list:      
        response = requests.post(url=url, headers=headers, json=payload)

        store_path = f'{self.name}/{crawl_type}.json'

        if response.status_code == 200:
            # Save the JSON response to a single file
            job_detail = response.json()
            try:
                # Load existing data if the file exists
                with open(store_path, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
            except FileNotFoundError:
                existing_data = []

            # Append the new job detail to the existing data
            existing_data.append(job_detail)

            # Save the updated data back to the file
            with open(store_path, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
            print(f"Job {crawl_type} appended to id.json")
        else:
            print(f"Failed to fetch the job{crawl_type}. Status code: {response.status_code}")


    def crawl_id_execute(self, url_value, headers_value,  payload_format, crawl_type_value, crawl_page: int = None, crawl_page_param: str = None, time_sleep: int = 8):
        # Load the last processed page number if it exists
        try:
            with open(f"{self.name}/last_processed_page.txt", "r") as file:
                start_page = int(file.read().strip()) + 1
        except FileNotFoundError:
            start_page = 1

        current_page = start_page
        while current_page <= crawl_page:

            for key, value in payload_format.items():
                if key == crawl_page_param:
                    payload_format[key] = current_page
                    break
                else:
                    for k, v in value.items():
                        if k == crawl_page_param:
                            payload_format[key][k] = current_page
                            break
                break
            
            # print(payload_format)
            payload_value = payload_format

            try:
                self.crawl_fuc(url=url_value,
                               headers=headers_value,
                               payload=payload_value,
                               crawl_type=crawl_type_value)
            except Exception as e:
                print(f"Error on page {current_page}: {e}")
                print("Retrying after 5 seconds...")
                time.sleep(time_sleep)
                continue  # Retry the same page after sleeping

            # Save the last successfully processed page
            with open(f"{self.name}/last_processed_page.txt", "w") as file:
                file.write(str(current_page))
            current_page += 1
        
    def crawl_job_detail_execute(self, url_value, headers_value, payload_format, crawl_type_value, job_id_list: list, job_id_param: str = None, time_sleep: int = 8):
        # Load the list of last processed job IDs if it exists
        try:
            with open(f"{self.name}/last_processed_jobs.json", "r") as file:
                processed_jobs = json.load(file)
        except FileNotFoundError:
            processed_jobs = []

        for job_id in job_id_list:
            if job_id in processed_jobs:
                continue  # Skip already processed jobs

            success = False
            while not success:
                try:
                    # Update the payload with the current job ID
                    for key, value in payload_format.items():
                        if key == job_id_param:
                            payload_format[key] = job_id
                            break
                        else:
                            for k, v in value.items():
                                if k == job_id_param:
                                    payload_format[key][k] = job_id
                                    break
                        break
                                        
                    # Call the crawl function
                    self.crawl_fuc(url=url_value,
                                   headers=headers_value,
                                   payload=payload_format,
                                   crawl_type=crawl_type_value)

                    # Add the successfully processed job ID to the list
                    processed_jobs.append(job_id)

                    # Save the updated list of processed job IDs
                    with open(f"{self.name}/last_processed_jobs.json", "w") as file:
                        json.dump(processed_jobs, file, ensure_ascii=False, indent=4)

                    success = True
                except Exception as e:
                    print(f"Error processing job ID {job_id}: {e}")
                    print("Retrying after 5 seconds...")
                    time.sleep(time_sleep)

    
    def meituan_id_process(self,id_path:str,job_id_param:str) -> list:
        id_path = f'{self.name}/{id_path}'
        with open(id_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        job_id_list = []

        for data in data:
            for value in data['data']['list']:
                job_id_list.append(value[job_id_param])
        
        with open(f'{self.name}/job_id.json','w') as f:
            json.dump(job_id_list,f)

        return job_id_list
                    