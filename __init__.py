import os
import subprocess
import cv2


class VideoBasler:

    def __init__(self, feature_config="config.pfs", use_opencv=False):
        module_root = os.path.dirname(__file__)
        pipefile = 'opencv.pipe' if use_opencv else 'basler.pipe'
        target = 'opencv.tiff' if use_opencv else 'basler.tiff'
        self.pipefile = os.path.join(module_root, pipefile)
        if not os.path.exists(self.pipefile):
            os.mkfifo(self.pipefile)
        self.target = os.path.join(module_root, target)
        proc_path = './' if module_root is '' else module_root
        proc_exec = 'video_opencv' if use_opencv else 'video_basler'
        if use_opencv:
            self.proc = subprocess.Popen(
                [os.path.join(proc_path, proc_exec), self.pipefile, self.target])
        else:
            self.proc = subprocess.Popen(
                [os.path.join(proc_path, proc_exec), self.pipefile, self.target, feature_config])

    def read(self):
        with open(self.pipefile, 'w') as pipe:
            pipe.write('request')
        with open(self.pipefile, 'r') as pipe:
            status = pipe.read().strip()
        if status == 'success':
            img = cv2.imread(self.target)
            if img is not None:
                return True, img
        return False, None

    def close(self):
        with open(self.pipefile, 'w') as pipe:
            pipe.write('stop')
        os.remove(self.pipefile)
        os.remove(self.target)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-opencv', action='store_true')
    #parser.add_argument('--exposure-time', default=100000)
    parser.add_argument('--feature-config', default='config.pfs')
    parser.add_argument('--N', type=float, default=3.5)
    args = parser.parse_args()
    cap = VideoBasler(feature_config=args.feature_config, use_opencv=args.use_opencv)
    while True:
        status, img = cap.read()
        if status:
            height, width = img.shape[:2]
            vis = cv2.resize(img, (int(width / args.N), int(height / args.N)))
            cv2.imshow('main of VideoBasler', vis)
            ch = 0xFF & cv2.waitKey(1)
            if ch == 27:
                cap.close()
                break
