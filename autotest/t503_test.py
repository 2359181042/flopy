import os
import shutil
import flopy
import pymake
import platform


def download_mf6_distribution():
    """
    Download mf6 distribution and return location of folder

    """

    # set url
    dirname = 'mf6.0.1'
    url = 'https://water.usgs.gov/ogw/modflow/{0}.zip'.format(dirname)

    # create folder for mf6 distribution download
    cpth = os.getcwd()
    dstpth = os.path.join('temp', 'mf6dist')
    print('create...{}'.format(dstpth))
    if not os.path.exists(dstpth):
        os.makedirs(dstpth)
    os.chdir(dstpth)

    # Download the distribution
    pymake.download_and_unzip(url, verify=True)

    # change back to original path
    os.chdir(cpth)

    # return the absolute path to the distribution
    mf6path = os.path.abspath(os.path.join(dstpth, dirname))

    return mf6path


def test_load_mf6_distribution_models():

    out_dir = os.path.join('temp', 't503')
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    mf6path = download_mf6_distribution()
    distpth = os.path.join(mf6path, 'examples')
    folders = [f for f in os.listdir(distpth)
               if os.path.isdir(os.path.join(distpth, f))]

    for f in folders:
        src = os.path.join(distpth, f)
        dst = os.path.join(out_dir, f)
        print('copying {}'.format(f))
        shutil.copytree(src, dst)

    exe_name = 'mf6'
    for f in folders:
        folder = os.path.join(out_dir, f)
        print('loading {}'.format(folder))
        sim = flopy.mf6.MFSimulation.load(f, 'mf6', exe_name, folder)
        assert isinstance(sim, flopy.mf6.MFSimulation)


if __name__ == '__main__':
    test_load_mf6_distribution_models()
