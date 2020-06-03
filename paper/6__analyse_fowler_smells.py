from pathlib import Path

import functools
import os
import traceback
from multiprocessing import Pool

import pandas as pd

from config import Config
from metrics.version_metrics_data import DataBuilder
from metrics.version_metrics_name import DataName
from projects import ProjectName


done = [
]


def build_dataset(version, project, slog, flog, fvlog):
    print("building {0}:{1}".format(project.github(), version))
    try:
        db = DataBuilder(project, version)
        db.append(DataName.ImperativeAbstraction)
        db.append(DataName.MultifacetedAbstraction)
        db.append(DataName.UnnecessaryAbstraction)
        db.append(DataName.UnutilizedAbstraction)
        db.append(DataName.DeficientEncapsulation)
        db.append(DataName.UnexploitedEncapsulation)
        db.append(DataName.BrokenModularization)
        db.append(DataName.Cyclic_DependentModularization)
        db.append(DataName.InsufficientModularization)
        db.append(DataName.Hub_likeModularization)
        db.append(DataName.BrokenHierarchy)
        db.append(DataName.CyclicHierarchy)
        db.append(DataName.DeepHierarchy)
        db.append(DataName.MissingHierarchy)
        db.append(DataName.MultipathHierarchy)
        db.append(DataName.RebelliousHierarchy)
        db.append(DataName.WideHierarchy)
        db.append(DataName.Bugged)
        classes_df, methods_df = db.build()
        print("succeeded to build {0}:{1}\n".format(
            project.github(),
            version))
        slog.write("succeeded to build {0}:{1}\n".format(
            project.github(),
            version))
        # TODO Join both so that the method and the class are fixed
        df = classes_df + methods_df
        return df
    except Exception as e:
        print("failed to build {0}:{1}\n".format(
            project.github,
            version))
        flog.write("failed to build {0}:{1}\n".format(
            project.github,
            version))
        fvlog.write("failed to build {0}:{1}\n {2}\n{3}\n\n").format(
                project.github(),
                version,
                e,
                traceback.format_exc())
        return None


def execute(project):
    dir = Config.get_work_dir_path(os.path.join("paper", "logs"))
    slog = open(os.path.join(dir, "(4)_success_xm.log"), "a")
    flog = open(os.path.join(dir, "(4)_failed_xm.log"), "a")
    fvlog = open(os.path.join(dir, "(4)_failed_verbose_xm.log"), "a")

    versions_dir = Config.get_work_dir_path(os.path.join("paper", "versions"))
    versions_path = os.path.join(versions_dir, project.github() + ".csv")
    versions = pd.read_csv(versions_path)['version'].to_list()
    build = functools.partial(build_dataset,
                                project=project,
                                slog=slog,
                                flog=flog,
                                fvlog=fvlog)

    dfs = list(map(build, versions))

    slog.close()
    flog.close()
    fvlog.close()

    if None in dfs:
        print("project " + project.github() + " failed")
        return

    df = pd.concat(dfs, axis=0, ignore_index=False)

    dir = Config.get_work_dir_path(os.path.join("paper", "datasets"))
    Path(dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(dir, project.github()+"_designite" + ".csv")
    df.to_csv(path)


if __name__ == "__main__":
    projects = list(ProjectName)
    projects = list(filter(lambda x: x not in done, projects))
    with Pool() as p:
        ris = p.map(execute, projects)
        print(ris)
