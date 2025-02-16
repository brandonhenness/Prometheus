"use client";
import {
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownSection,
  DropdownTrigger,
} from "@nextui-org/react";
import React, { useState } from "react";
import { AcmeIcon } from "../icons/acme-icon";
import { AcmeLogo } from "../icons/acmelogo";
import { GHCIcon } from "../icons/ghc-icon";
import { BottomIcon } from "../icons/sidebar/bottom-icon";

interface College {
  name: string;
  location: string;
  logo: React.ReactNode;
}

export const CollegesDropdown = () => {
  const [college, setCollege] = useState<College>({
    name: "Grays Harbor College",
    location: "SCCC Aberdeen, WA",
    logo: <GHCIcon />,
  });

  // A helper to wrap logos so they remain a fixed size.
  const LogoWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="w-8 h-8 flex-shrink-0">{children}</div>
  );

  return (
    // Use full width for the dropdown so it scales with its container
    <Dropdown classNames={{ base: "w-full" }}>
      <DropdownTrigger className="cursor-pointer">
        <div className="flex items-center gap-2 w-full">
          {/* Logo stays fixed size */}
          <div className="flex-shrink-0">
            <LogoWrapper>{college.logo}</LogoWrapper>
          </div>
          {/* Text container is allowed to shrink */}
          <div className="flex-grow min-w-0">
            <h3 className="text-xl font-medium m-0 text-default-900 truncate">
              {college.name}
            </h3>
            <span className="text-xs font-medium text-default-500 truncate">
              {college.location}
            </span>
          </div>
          {/* Chevron is fixed so it never shrinks */}
          <div className="flex-shrink-0">
            <BottomIcon />
          </div>
        </div>
      </DropdownTrigger>
      <DropdownMenu
        onAction={(key) => {
          if (key === "1") {
            setCollege({
              name: "Grays Harbor College",
              location: "SCCC Aberdeen, WA",
              logo: <GHCIcon />,
            });
          }
          if (key === "2") {
            setCollege({
              name: "Olympic College",
              location: "Bremerton, WA",
              logo: <AcmeLogo />,
            });
          }
          if (key === "3") {
            setCollege({
              name: "Seattle Central College",
              location: "Seattle, WA",
              logo: <AcmeIcon />,
            });
          }
          if (key === "4") {
            setCollege({
              name: "Tacoma Community College",
              location: "Tacoma, WA",
              logo: <AcmeIcon />,
            });
          }
        }}
        aria-label="College Selection"
      >
        <DropdownSection title="Colleges">
          <DropdownItem
            key="1"
            startContent={<LogoWrapper><GHCIcon /></LogoWrapper>}
            description="SCCC Aberdeen, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold truncate",
            }}
          >
            Grays Harbor College
          </DropdownItem>
          <DropdownItem
            key="2"
            startContent={<LogoWrapper><AcmeLogo /></LogoWrapper>}
            description="Bremerton, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold truncate",
            }}
          >
            Olympic College
          </DropdownItem>
          <DropdownItem
            key="3"
            startContent={<LogoWrapper><AcmeIcon /></LogoWrapper>}
            description="Seattle, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold truncate",
            }}
          >
            Seattle Central College
          </DropdownItem>
          <DropdownItem
            key="4"
            startContent={<LogoWrapper><AcmeIcon /></LogoWrapper>}
            description="Tacoma, WA"
            classNames={{
              base: "py-4",
              title: "text-base font-semibold truncate",
            }}
          >
            Tacoma Community College
          </DropdownItem>
        </DropdownSection>
      </DropdownMenu>
    </Dropdown>
  );
};
