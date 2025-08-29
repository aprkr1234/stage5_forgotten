import zipfile # 표준 파이썬 zipfile 모듈: zip 파일 열기 및 추출 작업 지원
import time # 표준 파이썬 time 모듈: 시간 측정 및 진행 시간 확인 용도

def unlock_zip(zip_path):
    """
    주어진 zip 파일의 비밀번호를 무차별 대입 방식(brute-force)으로 찾아내는 함수.
    비밀번호는 소문자와 숫자로만 이루어진 6자리 문자열임을 알고 있음.
    성공 시 password.txt에 비밀번호 저장, 진행 중 다양한 정보(시작 시각/반복 회수/경과 시간) 출력.
    실패/오류 발생 시 예외 메시지 처리.
    :param zip_path: 암호화된 zip 파일 경로(문자열)
    """
    start_time = time.time() # 함수 시작 시각(초 단위, float) 저장
    count = 0 # 시도한 비밀번호 총 개수 집계 변수(최종 통계용)
    found = False # 비밀번호를 찾았는지 여부(True면 즉시 모든 반복문 중단)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789' # 사용 가능한 문자: 소문자+숫자
    password = '' # 정답 비밀번호를 저장할 변수(초기에는 빈 문자열)
    
    # 진행상황 출력을 위한 변수들
    total_combinations = len(chars) ** 6  # 전체 조합 수: 36^6
    progress_interval = 100000  # 10만번마다 진행상황 출력
    last_progress_time = start_time  # 마지막 진행상황 출력 시각
    
    print(f"브루트포스 공격 시작! 총 {total_combinations:,}개 조합 확인 예정...")
    print(f"진행상황은 {progress_interval:,}번마다 출력됩니다.")
    print("-" * 60)
    
    try:
        # zip 파일을 열기 시도. 존재하지 않거나 비정상 파일이면 예외 발생(Exception 핸들링 됨)
        with zipfile.ZipFile(zip_path) as zf:
            # 아래 여섯 개의 중첩된 for문을 통해 모든 6자리 alpha-numeric 조합 생성
            # 총 36^6 = 2,176,782,336 개의 가능성(매우 많으므로 실제 사용시 시간 주의)
            for a in chars:
                for b in chars:
                    for c in chars:
                        for d in chars:
                            for e in chars:
                                for f in chars:
                                    # 현재 6개의 문자로 비밀번호 조합 생성
                                    pwd = a + b + c + d + e + f
                                    count += 1 # 비밀번호 시도 횟수 1증가
                                    
                                    # 진행상황 출력 (일정 간격마다)
                                    if count % progress_interval == 0:
                                        current_time = time.time()
                                        elapsed = current_time - start_time
                                        progress_percent = (count / total_combinations) * 100
                                        passwords_per_sec = count / elapsed if elapsed > 0 else 0
                                        remaining_combinations = total_combinations - count
                                        eta_seconds = remaining_combinations / passwords_per_sec if passwords_per_sec > 0 else 0
                                        
                                        print(f"진행률: {progress_percent:.2f}% | "
                                              f"시도: {count:,}/{total_combinations:,} | "
                                              f"현재 비밀번호: {pwd} | "
                                              f"속도: {passwords_per_sec:.0f} pwd/sec | "
                                              f"경과시간: {elapsed:.1f}초 | "
                                              f"예상 완료: {eta_seconds/60:.1f}분")
                                        last_progress_time = current_time
                                    
                                    try:
                                        # 비밀번호를 바이트(byte) 형태로 변환(utf-8 인코딩 -> zipfile 요구사항)
                                        # 성공하면 압축파일 내용이 정상적으로 추출됨
                                        zf.extractall(pwd=bytes(pwd, 'utf-8'))
                                        # 추출 성공(예외 발생 없음): 정답 비밀번호 발견!
                                        found = True
                                        password = pwd # 찾아낸 비밀번호 저장
                                        print(f"\n🎉 비밀번호 발견! : {pwd}")
                                        break # 가장 안쪽 반복문 즉시 종료
                                    except:
                                        # 비밀번호가 틀릴 경우 압축파일 추출에서 예외 발생
                                        # 아무 일 없었던 듯 다음 비밀번호 조합을 계속 시도
                                        pass
                                # 안쪽에서 비밀번호 찾았으면 반복문 탈출(효율적 중단 구현)
                                if found:
                                    break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
                    
        # 반복이 모두 끝난 뒤 결과 및 실행 정보 요약해서 출력(작업 시작 시각, 반복 횟수, 경과 시간)
        print("\n" + "="*60)
        print('Started at:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
        print('Tried:', f"{count:,}", 'passwords')
        print('Total time:', f"{time.time() - start_time:.2f}", 'seconds')
        
        if found:
            # 정답 비밀번호 password.txt로 저장(새 파일 생성/기존 덮어씀)
            with open('password.txt', 'w') as f:
                f.write(password)
            print('✅ Password found:', password) # stdout으로 비밀번호 출력
            print('📁 비밀번호가 password.txt 파일에 저장되었습니다.')
        else:
            # 모든 경우를 확인했지만 정답을 못 찾았을 경우 안내문자 출력
            print('❌ Password NOT found.')
            
    except Exception as e:
        # 파일 열기/읽기/쓰기 등 예상하지 못한 문제(ex: 파일 경로 오류)를 처리
        print('Error:', e) # 예외 정보(에러 메시지) 출력

# 함수 사용 예시(실행 시 파일 경로 넣어 사용)
# unlock_zip('emergency_storage_key.zip')
