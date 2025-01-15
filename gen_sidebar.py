from pathlib import Path

EXCLUDE_DIR = {'FILES', '.git', '_assets', '草稿', '归档'}
SORT = ['Python', 'Go', '前端', '折腾', '逆向工程', ' 杂谈', '其他', 'coding']


def gen_sub(p: Path, deepth: int = 0, prefix_idx: str = '') -> list[str]:
    ret = []
    i = 1
    for fp in p.iterdir():
        if fp.is_dir():
            if fp.name in EXCLUDE_DIR:
                continue
            children = gen_sub(fp, deepth=deepth + 1, prefix_idx=f'{prefix_idx}{i}.')
            ret.append(f'{deepth * "\t"}* [{prefix_idx}{i} {fp.name}]({fp})')
            ret.extend(children)
            i += 1
        else:
            ret.append(f'{deepth * "\t"}* [{fp.name.removesuffix('.md')}]({fp})')
            i += 1
    return sorted(ret)


def sort_by(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda p: SORT.index(p.name) if p.name in SORT else 0)


def gen():
    ret = []
    i = 1
    for p in sort_by(list(Path('.').iterdir())):
        if p.is_dir():
            if p.name in EXCLUDE_DIR:
                continue
            if p.name.startswith(('_', '.')):
                continue
            ret.append(f'* {p.name}')
            ret.extend(gen_sub(p, 1, f'{i}.'))
            i += 1

    with Path('_sidebar.md').open('w') as f:
        f.write('\n'.join(ret))


if __name__ == '__main__':
    gen()
