import os
from datetime import datetime
import datetime as date_delta
import concurrent.futures

def check_path_store_v2(path_used, filename):
    # if filename.endswith('.pdf'):
    abs_path_file = os.path.join(path_used, filename)
    time_update = int(os.path.getmtime(abs_path_file))
    timestamp = datetime.fromtimestamp(time_update)
    last_modified = str(timestamp).split(" ")[0]

    return filename


def extract_all():
    data = []
    path_used = "/media/b2b/rexbridge-b2b.com/uploads/bataras/"
    obj = os.scandir(path_used)
    with concurrent.futures.ProcessPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_path_store_v2, path_used, filename): filename for filename in os.listdir(path_used)}
        #print('THREADS USED:', len(executor._threads))
        #print('pending:', executor._work_queue.qsize(), 'jobs')
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result != None:
                    data.append(result)
            except Exception as exc:
                print("There was an error. {}".format(exc))
    print(data)
    print(len(data))
    return data



if __name__ == '__main__':
    results = extract_all()
