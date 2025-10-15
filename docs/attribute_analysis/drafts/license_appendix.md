# License Field Analysis Appendix

This is an extraction from the https://packages.ecosyste.ms/ service, analyzing the top 9 registries by package count and examining the most commonly used licenses across all active packages. This analysis uses the raw `licenses` field as reported by each package registry, with the analysis covering both the general package population and packages marked as critical infrastructure.

Code for this script lives here: https://github.com/ecosyste-ms/packages/blob/main/lib/tasks/license_analysis.rake

## Global Analysis
Total packages: 9,671,935

### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 3,031,054 | 31.34% |
| '' | 1,919,350 | 19.84% |
| NULL | 1,227,701 | 12.69% |
| ISC | 1,109,627 | 11.47% |
| Apache-2.0 | 490,475 | 5.07% |
| MIT License | 152,735 | 1.58% |
| BSD-3-Clause | 125,015 | 1.29% |
| The Apache Software License, Version 2.0 | 88,919 | 0.92% |
| GPL-3.0 | 73,014 | 0.75% |
| Apache-2.0,Apache-2.0 | 61,429 | 0.64% |
| Apache License, Version 2.0 | 52,548 | 0.54% |
| GPL-2.0-or-later | 46,678 | 0.48% |
| The Apache License, Version 2.0 | 45,312 | 0.47% |
| GPL-3.0-or-later | 41,066 | 0.42% |
| MIT OR Apache-2.0 | 39,979 | 0.41% |
| BSD | 36,975 | 0.38% |
| BSD-2-Clause | 36,583 | 0.38% |
| MPL-2.0 | 33,983 | 0.35% |
| Apache 2.0 | 26,934 | 0.28% |
| perl_5 | 22,881 | 0.24% |

## Per Registry Analysis

### npmjs.org (npm)
Total packages: 3,397,287

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 1,545,632 | 45.5% |
| ISC | 1,093,729 | 32.19% |
| '' | 408,629 | 12.03% |
| Apache-2.0 | 123,151 | 3.62% |
| UNLICENSED | 20,953 | 0.62% |
| BSD-3-Clause | 18,787 | 0.55% |
| GPL-3.0 | 16,107 | 0.47% |
| CC BY-NC-SA 4.0 | 9,454 | 0.28% |
| SEE LICENSE IN LICENSE | 9,049 | 0.27% |
| BSD | 8,687 | 0.26% |

### proxy.golang.org (go)
Total packages: 1,733,758

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| '' | 747,219 | 43.1% |
| MIT | 390,479 | 22.52% |
| NULL | 225,389 | 13.0% |
| Apache-2.0 | 209,784 | 12.1% |
| BSD-3-Clause | 42,848 | 2.47% |
| GPL-3.0 | 42,430 | 2.45% |
| BSD-2-Clause | 14,592 | 0.84% |
| MPL-2.0 | 14,046 | 0.81% |
| AGPL-3.0 | 10,281 | 0.59% |
| Unlicense | 6,059 | 0.35% |

### hub.docker.com (docker)
Total packages: 831,374

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| NULL | 831,374 | 100.0% |

### nuget.org (nuget)
Total packages: 650,205

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| '' | 487,022 | 74.9% |
| MIT | 120,560 | 18.54% |
| Apache-2.0 | 22,154 | 3.41% |
| LGPL-3.0-only | 4,412 | 0.68% |
| BSD-3-Clause | 2,158 | 0.33% |
| GPL-3.0-or-later | 1,795 | 0.28% |
| LGPL-3.0-or-later | 1,418 | 0.22% |
| MS-PL | 1,405 | 0.22% |
| GPL-3.0-only | 1,244 | 0.19% |
| AGPL-3.0-or-later | 768 | 0.12% |

### pypi.org (pypi)
Total packages: 712,758

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 171,490 | 24.06% |
| '' | 151,225 | 21.22% |
| MIT License | 116,716 | 16.38% |
| UNKNOWN | 16,587 | 2.33% |
| BSD | 16,145 | 2.27% |
| AGPL-3 | 16,033 | 2.25% |
| Other/Proprietary License | 15,443 | 2.17% |
| Apache-2.0 | 13,698 | 1.92% |
| Apache Software License | 12,194 | 1.71% |
| Apache License 2.0 | 8,850 | 1.24% |

### repo1.maven.org (maven)
Total packages: 557,789

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| The Apache Software License, Version 2.0 | 88,271 | 15.83% |
| Apache-2.0,Apache-2.0 | 60,385 | 10.83% |
| MIT | 45,930 | 8.23% |
| The Apache License, Version 2.0 | 44,966 | 8.06% |
| Apache License, Version 2.0 | 44,787 | 8.03% |
| Apache-2.0 | 37,718 | 6.76% |
| MIT License | 33,051 | 5.93% |
| '' | 13,694 | 2.46% |
| Apache 2 | 11,639 | 2.09% |
| Apache License 2.0 | 10,796 | 1.94% |

### packagist.org (packagist)
Total packages: 425,124

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 280,430 | 65.96% |
| '' | 39,888 | 9.38% |
| BSD-3-Clause | 17,853 | 4.2% |
| Apache-2.0 | 15,126 | 3.56% |
| proprietary | 10,667 | 2.51% |
| GPL-2.0-or-later | 7,808 | 1.84% |
| GPL-3.0-or-later | 6,227 | 1.46% |
| GPL-3.0 | 3,860 | 0.91% |
| OSL-3.0,AFL-3.0 | 3,647 | 0.86% |
| GPL-2.0+ | 3,075 | 0.72% |

### crates.io (cargo)
Total packages: 200,290

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 83,944 | 41.91% |
| MIT OR Apache-2.0 | 38,430 | 19.19% |
| Apache-2.0 | 24,292 | 12.13% |
| non-standard | 7,935 | 3.96% |
| MIT/Apache-2.0 | 7,513 | 3.75% |
| MPL-2.0 | 4,236 | 2.11% |
| GPL-3.0 | 3,898 | 1.95% |
| GPL-3.0-or-later | 2,866 | 1.43% |
| BSD-3-Clause | 2,809 | 1.4% |
| Apache-2.0 OR MIT | 2,724 | 1.36% |

### rubygems.org (rubygems)
Total packages: 185,563

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 99,086 | 53.4% |
| '' | 33,721 | 18.17% |
| NULL | 33,268 | 17.93% |
| Apache-2.0 | 5,306 | 2.86% |
| Apache 2.0 | 989 | 0.53% |
| GPL-3.0 | 888 | 0.48% |
| BSD-3-Clause | 722 | 0.39% |
| Apache License (2.0) | 587 | 0.32% |
| BSD | 548 | 0.3% |
| BSD-2-Clause | 538 | 0.29% |

## Critical Packages Global Analysis
Total critical packages: 9,774

### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 4,135 | 42.31% |
| Apache-2.0 | 1,000 | 10.23% |
| BSD-3-Clause | 939 | 9.61% |
| MIT OR Apache-2.0 | 349 | 3.57% |
| NULL | 320 | 3.27% |
| '' | 283 | 2.9% |
| Apache License, Version 2.0 | 181 | 1.85% |
| ISC | 164 | 1.68% |
| BSD-2-Clause | 159 | 1.63% |
| MIT + file LICENSE | 143 | 1.46% |

## Critical Packages Per Registry Analysis

### npmjs.org (npm)
Total critical packages: 2,289

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 1,834 | 80.12% |
| Apache-2.0 | 172 | 7.51% |
| ISC | 132 | 5.77% |
| BSD-3-Clause | 57 | 2.49% |
| BSD-2-Clause | 38 | 1.66% |

### proxy.golang.org (go)
Total critical packages: 645

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 256 | 39.69% |
| Apache-2.0 | 210 | 32.56% |
| BSD-3-Clause | 102 | 15.81% |
| BSD-2-Clause | 25 | 3.88% |
| MPL-2.0 | 23 | 3.57% |

### hub.docker.com (docker)
Total critical packages: 143

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| NULL | 143 | 100.0% |

### nuget.org (nuget)
Total critical packages: 376

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 177 | 47.07% |
| '' | 156 | 41.49% |
| Apache-2.0 | 36 | 9.57% |
| BSD-3-Clause | 4 | 1.06% |
| Apache-2.0 OR MPL-2.0 | 1 | 0.27% |

### pypi.org (pypi)
Total critical packages: 523

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| '' | 80 | 15.3% |
| MIT | 76 | 14.53% |
| MIT License | 70 | 13.38% |
| Apache 2.0 | 37 | 7.07% |
| BSD License | 31 | 5.93% |

### repo1.maven.org (maven)
Total critical packages: 704

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| Apache License, Version 2.0 | 160 | 22.73% |
| The Apache Software License, Version 2.0 | 110 | 15.63% |
| Apache-2.0,Apache-2.0 | 81 | 11.51% |
| Apache-2.0 | 52 | 7.39% |
| The Apache License, Version 2.0 | 20 | 2.84% |

### packagist.org (packagist)
Total critical packages: 548

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 419 | 76.46% |
| BSD-3-Clause | 69 | 12.59% |
| Apache-2.0 | 21 | 3.83% |
| BSD-2-Clause | 9 | 1.64% |
| BSD-3-Clause,GPL-2.0-only,GPL-3.0-only | 7 | 1.28% |

### crates.io (cargo)
Total critical packages: 813

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT OR Apache-2.0 | 348 | 42.8% |
| MIT | 177 | 21.77% |
| MIT/Apache-2.0 | 82 | 10.09% |
| Apache-2.0 OR MIT | 70 | 8.61% |
| Apache-2.0 | 38 | 4.67% |

### rubygems.org (rubygems)
Total critical packages: 974

#### Top licenses values:
| License | Count | Percentage |
|---------|-------|------------|
| MIT | 565 | 58.01% |
| Apache-2.0 | 288 | 29.57% |
| Ruby,BSD-2-Clause | 19 | 1.95% |
| BSD-2-Clause | 12 | 1.23% |
| '' | 11 | 1.13% |
