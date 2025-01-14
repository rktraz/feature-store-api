/*
 * Copyright (c) 2021 Logical Clocks AB
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *
 * See the License for the specific language governing permissions and limitations under the License.
 */

package com.logicalclocks.hsfs.metadata;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@JsonIgnoreProperties(ignoreUnknown = true)
@NoArgsConstructor
@AllArgsConstructor
public class Code extends RestDto<Code> {

  @Getter
  @Setter
  private Long commitTime;

  @Getter
  @Setter
  private Long featureGroupCommitId;

  @Getter
  @Setter
  private String applicationId;

  @Getter
  @Setter
  private String content;

  public Code(Long commitTime, String applicationId) {
    this.commitTime = commitTime;
    this.applicationId = applicationId;
  }

  public enum RunType {
    JUPYTER,
    JOB,
    DATABRICKS;
  }
}

